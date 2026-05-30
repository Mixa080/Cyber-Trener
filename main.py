import cv2
from ultralytics import YOLO
import cvzone
import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
import speech_recognition as sr
import threading
import datetime
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from database import get_db_connection
from utils import speak_async, calculate_angle, draw_centered_transparent_text, CameraThread

import hashlib
import settings_manager

user_settings = settings_manager.load_settings()
ctk.set_appearance_mode(user_settings.get("appearance", "Dark"))
ctk.set_default_color_theme(user_settings.get("theme", "green"))


class CyberTrenerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Cyber Trener - Digital Twin")
        self.geometry("1100x800")
        self.minsize(900, 700)
        self.configure(fg_color=("#F9F8F6", "#242424"))



        self.current_user_id = None
        self.current_username = ""
        self.rep_count = 0
        self.stage = None
        self.is_training = False
        self.cap = None
        self.start_time = 0

        self.pose_model = YOLO('yolov8n-pose.pt')

        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True)

        self.show_login_screen()

    def clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def show_login_screen(self):
        self.clear_container()

        login_frame = ctk.CTkFrame(self.container, corner_radius=15, width=400, height=450, fg_color=("#FFFFFF", "#2b2b2b"))
        login_frame.place(relx=0.5, rely=0.5, anchor="center")
        login_frame.pack_propagate(False)

        ctk.CTkLabel(login_frame, text="Logowanie", font=ctk.CTkFont(size=28, weight="bold")).pack(pady=(40, 30))

        self.user_entry = ctk.CTkEntry(login_frame, placeholder_text="Nazwa użytkownika", width=250, height=40,
                                       font=ctk.CTkFont(size=14))
        self.user_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(login_frame, placeholder_text="Hasło (opcjonalne)", show="*", width=250, height=40,
                     font=ctk.CTkFont(size=14))
        self.password_entry.pack(pady=10)

        ctk.CTkButton(login_frame, text="Zapomniałem hasła?", width=200, height=20, 
                      fg_color="transparent", hover_color=("#E5E4E0", "#2b2b2b"), text_color=("#6B6B6B", "#A0A0A0"),
                      font=ctk.CTkFont(size=12, underline=True),
                      command=self.show_reset_password_dialog).pack(pady=5)

        ctk.CTkButton(login_frame, text="Zaloguj / Zarejestruj", width=250, height=45,
                      font=ctk.CTkFont(size=16, weight="bold"),
                      command=self.process_login).pack(pady=(40, 20))

    def process_login(self):
        username = self.user_entry.get().strip()
        password = self.password_entry.get()
        if not username:
            speak_async("Proszę podać nazwę użytkownika")
            return

        pwd_hash = hashlib.sha256(password.encode()).hexdigest() if password else None

        conn = get_db_connection()
        if not conn:
            speak_async("Błąd połączenia z bazą serwera")
            return

        c = conn.cursor()
        c.execute("SELECT id, username, password_hash FROM users WHERE username = ?", (username,))
        user = c.fetchone()

        if user:
            db_hash = user[2]
            if db_hash and not password:
                speak_async("To konto wymaga hasła.")
                conn.close()
                return
            if db_hash and db_hash != pwd_hash:
                speak_async("Nieprawidłowe hasło.")
                conn.close()
                return

            self.current_user_id = user[0]
            self.current_username = user[1]
            speak_async(f"Witaj ponownie, {self.current_username}")
        else:
            c.execute("INSERT INTO users (username, password_hash) OUTPUT INSERTED.id VALUES (?, ?)", (username, pwd_hash))
            new_id = c.fetchone()[0]
            conn.commit()
            self.current_user_id = int(new_id)
            self.current_username = username
            speak_async(f"Konto utworzone. Witaj, {self.current_username}")

        conn.close()
        self.show_dashboard_screen()

    def show_reset_password_dialog(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Reset Hasła")
        dialog.geometry("300x250")
        dialog.attributes("-topmost", True)
        
        ctk.CTkLabel(dialog, text="Zresetuj Hasło", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)
        user_input = ctk.CTkEntry(dialog, placeholder_text="Nazwa użytkownika")
        user_input.pack(pady=10)
        pass_input = ctk.CTkEntry(dialog, placeholder_text="Nowe hasło", show="*")
        pass_input.pack(pady=10)
        
        def save_new_password():
            username = user_input.get().strip()
            new_password = pass_input.get()
            if not username or not new_password:
                speak_async("Podaj nazwę użytkownika i nowe hasło.")
                return
            
            pwd_hash = hashlib.sha256(new_password.encode()).hexdigest()
            conn = get_db_connection()
            if conn:
                c = conn.cursor()
                c.execute("UPDATE users SET password_hash = ? WHERE username = ?", (pwd_hash, username))
                if c.rowcount > 0:
                    speak_async("Hasło zostało zaktualizowane.")
                    dialog.destroy()
                else:
                    speak_async("Nie znaleziono takiego użytkownika.")
                conn.commit()
                conn.close()
            else:
                speak_async("Błąd połączenia z bazą.")
        
        ctk.CTkButton(dialog, text="Zapisz nowe hasło", command=save_new_password).pack(pady=15)

    def show_dashboard_screen(self):
        if hasattr(self, 'user_entry') and self.user_entry.winfo_exists():
            self.current_user = self.user_entry.get()

        self.clear_container()

        header = ctk.CTkFrame(self.container, height=70, corner_radius=0, fg_color=("#EAE9E4", "#1f1f1f"))
        header.pack(fill="x", side="top")
        ctk.CTkLabel(header, text=f"Witaj, {self.current_username}!", font=ctk.CTkFont(size=22, weight="bold")).pack(
            side="left", padx=30, pady=20)
        ctk.CTkButton(header, text="Wyloguj", width=100, fg_color="#E53935", hover_color="#C62828",
                      command=self.show_login_screen).pack(side="right", padx=30, pady=20)

        tabview = ctk.CTkTabview(self.container, width=1000, height=500)
        tabview.pack(fill="both", expand=True, padx=40, pady=20)

        tab_summary = tabview.add("Podsumowanie")
        tab_history = tabview.add("Historia i Statystyki")

        self.build_summary_tab(tab_summary)
        self.build_history_tab(tab_history)

        bottom_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        bottom_frame.pack(fill="x", side="bottom", pady=20)

        ctk.CTkButton(bottom_frame, text="⚙ Ustawienia", height=40, width=300, fg_color=("#D4D3CF", "#555555"),
                      hover_color=("#C4C3BF", "#777777"), text_color=("#000000", "#FFFFFF"),
                      command=self.show_settings_dialog).pack(pady=5)

        ctk.CTkButton(bottom_frame, text="▶ Rozpocznij Trening", height=60, width=300,
                      font=ctk.CTkFont(size=20, weight="bold"),
                      command=self.start_training).pack(pady=10)
        ctk.CTkButton(bottom_frame, text="🎤 Nasłuchuj komend", height=40, width=300, fg_color="#FF9800",
                      hover_color="#F57C00", text_color="white",
                      command=self.listen_command).pack(pady=5)

    def show_settings_dialog(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Ustawienia")
        dialog.geometry("350x300")
        dialog.attributes("-topmost", True)
        
        current_settings = settings_manager.load_settings()
        
        ctk.CTkLabel(dialog, text="Ustawienia Aplikacji", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=(10, 20))
        
        ctk.CTkLabel(dialog, text="Motyw Aplikacji:").pack()
        appearance_var = ctk.StringVar(value=current_settings.get("appearance", "Dark"))
        appearance_menu = ctk.CTkOptionMenu(dialog, values=["Dark", "Light", "System"], variable=appearance_var)
        appearance_menu.pack(pady=(0, 15))
        
        voice_var = ctk.BooleanVar(value=current_settings.get("voice_enabled", True))
        voice_checkbox = ctk.CTkCheckBox(dialog, text="Asystent Głosowy (wymaga restartu)", variable=voice_var)
        voice_checkbox.pack(pady=10)
        
        def save():
            current_settings["appearance"] = appearance_var.get()
            current_settings["voice_enabled"] = voice_var.get()
            settings_manager.save_settings(current_settings)
            ctk.set_appearance_mode(current_settings["appearance"])
            speak_async("Ustawienia zostały zapisane.")
            dialog.destroy()
            
            if not getattr(self, 'is_training', False):
                self.show_dashboard_screen()
            
        ctk.CTkButton(dialog, text="Zapisz", fg_color="#4CAF50", hover_color="#388E3C", command=save).pack(pady=20)

    def build_summary_tab(self, parent):
        conn = get_db_connection()
        total_reps, total_workouts = 0, 0
        if conn:
            c = conn.cursor()
            c.execute("SELECT SUM(reps), COUNT(id) FROM workouts WHERE user_id = ?", (self.current_user_id,))
            stats = c.fetchone()
            conn.close()
            if stats:
                total_reps = stats[0] if stats[0] else 0
                total_workouts = stats[1] if stats[1] else 0

        left_col = ctk.CTkFrame(parent, corner_radius=15, fg_color=("#FFFFFF", "#2b2b2b"))
        left_col.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        ctk.CTkLabel(left_col, text="Szybki Przegląd", font=ctk.CTkFont(size=20, weight="bold"),
                     text_color="#4CAF50").pack(anchor="w", padx=20, pady=(20, 10))
        ctk.CTkLabel(left_col, text=f"🔥 Ukończone treningi: {total_workouts}", font=ctk.CTkFont(size=16)).pack(
            anchor="w", padx=20, pady=5)
        ctk.CTkLabel(left_col, text=f"💪 Łączna liczba powtórzeń: {total_reps}", font=ctk.CTkFont(size=16)).pack(
            anchor="w", padx=20, pady=5)

        right_col = ctk.CTkFrame(parent, corner_radius=15, fg_color=("#FFFFFF", "#2b2b2b"))
        right_col.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        ctk.CTkLabel(right_col, text="Plan na dziś", font=ctk.CTkFont(size=20, weight="bold"),
                     text_color="#2196F3").pack(anchor="w", padx=20, pady=(20, 10))
        ctk.CTkLabel(right_col, text="🎯 Ćwiczenie: Biceps z hantlami", font=ctk.CTkFont(size=16)).pack(anchor="w",
                                                                                                       padx=20, pady=5)
        ctk.CTkLabel(right_col, text="⏱ Cel: Skup się na płynnym ruchu", font=ctk.CTkFont(size=16)).pack(anchor="w",
                                                                                                         padx=20,
                                                                                                         pady=5)

    def build_history_tab(self, parent):
        history_frame = ctk.CTkScrollableFrame(parent, width=350, corner_radius=15, fg_color=("#FFFFFF", "#2b2b2b"),
                                               label_text="Ostatnie Treningi")
        history_frame.pack(side="left", fill="y", padx=10, pady=10)

        graph_frame = ctk.CTkFrame(parent, corner_radius=15, fg_color=("#FFFFFF", "#2b2b2b"))
        graph_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        conn = get_db_connection()
        dates_for_graph = []
        reps_for_graph = []

        if conn:
            c = conn.cursor()
            c.execute(
                "SELECT TOP 20 date, exercise_type, reps, duration_sec FROM workouts WHERE user_id = ? ORDER BY date DESC",
                (self.current_user_id,))
            rows = c.fetchall()

            if not rows:
                ctk.CTkLabel(history_frame, text="Brak historii treningów.", text_color=("#6B6B6B", "gray")).pack(pady=20)
            else:
                for row in rows:
                    date_str = row[0].strftime("%d.%m.%Y %H:%M")
                    record = ctk.CTkFrame(history_frame, fg_color=("#F9F8F6", "#333333"), corner_radius=10)
                    record.pack(fill="x", pady=5, padx=5)
                    ctk.CTkLabel(record, text=f"{date_str}", font=ctk.CTkFont(size=12, weight="bold"),
                                 text_color="#2196F3").pack(anchor="w", padx=10, pady=(5, 0))
                    ctk.CTkLabel(record, text=f"{row[1]} | {row[2]} powt. | {row[3]} sek",
                                 font=ctk.CTkFont(size=14)).pack(anchor="w", padx=10, pady=(0, 5))

            c.execute("""
                SELECT TOP 7 CAST(date AS DATE), SUM(reps) 
                FROM workouts 
                WHERE user_id = ? 
                GROUP BY CAST(date AS DATE) 
                ORDER BY CAST(date AS DATE) ASC
            """, (self.current_user_id,))
            graph_data = c.fetchall()
            conn.close()

            for g_row in graph_data:
                dates_for_graph.append(g_row[0].strftime("%d.%m"))
                reps_for_graph.append(g_row[1])

        if dates_for_graph:
            is_light = ctk.get_appearance_mode() == "Light"
            if is_light:
                plt.style.use('default')
                bg_color = '#FFFFFF'
                text_color = '#2D2D2D'
                grid_color = '#E5E4E0'
                spine_color = '#CCCCCC'
            else:
                plt.style.use('dark_background')
                bg_color = '#2b2b2b'
                text_color = 'white'
                grid_color = '#444444'
                spine_color = '#555555'

            fig = Figure(figsize=(5, 4), dpi=100)
            fig.patch.set_facecolor(bg_color)
            ax = fig.add_subplot(111)
            ax.set_facecolor(bg_color)

            ax.plot(dates_for_graph, reps_for_graph, color='#4CAF50', marker='o', linestyle='-', linewidth=2,
                    markersize=8)
            ax.fill_between(dates_for_graph, reps_for_graph, color='#4CAF50', alpha=0.2)

            ax.set_title('Postęp: Powtórzenia wg dni', color=text_color, pad=15)
            ax.tick_params(axis='x', colors=text_color)
            ax.tick_params(axis='y', colors=text_color)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['bottom'].set_color(spine_color)
            ax.spines['left'].set_color(spine_color)
            ax.grid(color=grid_color, linestyle='--', linewidth=0.5, alpha=0.7)

            fig.tight_layout()

            canvas = FigureCanvasTkAgg(fig, master=graph_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
        else:
            ctk.CTkLabel(graph_frame, text="Zrób pierwszy trening, aby zobaczyć wykres!", font=ctk.CTkFont(size=16),
                         text_color=("#6B6B6B", "gray")).pack(expand=True)

    def listen_command(self):
        def recognize():
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                speak_async("Słucham komendy...")
                try:
                    audio = recognizer.listen(source, timeout=3)
                    try:
                        command = recognizer.recognize_google(audio, language="pl-PL")
                    except sr.UnknownValueError:
                        command = recognizer.recognize_google(audio, language="en-US")
                    
                    if "trening" in command.lower() or "training" in command.lower() or "start" in command.lower():
                        self.after(0, self.start_training)
                except Exception:
                    pass

        threading.Thread(target=recognize, daemon=True).start()

    def start_training(self):
        self.is_training = True
        self.rep_count = 0
        self.stage = None
        self.start_time = time.time()
        
        self.frame_counter = 0
        self.last_results_front = None
        self.last_results_side = None

        self.clear_container()

        top_bar = ctk.CTkFrame(self.container, height=60, corner_radius=0, fg_color=("#EAE9E4", "#1f1f1f"))
        top_bar.pack(fill="x", side="top")

        ctk.CTkButton(top_bar, text="Zakończ trening", width=120, fg_color="#E53935", hover_color="#C62828",
                      command=self.stop_training).pack(side="left", padx=20, pady=15)

        self.info_label = ctk.CTkLabel(top_bar, text="Powtórzenia: 0  |  Technika: Gotowy",
                                       font=ctk.CTkFont(size=18, weight="bold"))
        self.info_label.pack(side="right", padx=30, pady=15)

        self.video_frame = ctk.CTkFrame(self.container, corner_radius=15, fg_color=("#FFFFFF", "#111111"))
        self.video_frame.pack(pady=20, padx=20, expand=True)
        bg_color = "#F9F8F6" if ctk.get_appearance_mode() == "Light" else "#0f172a"
        self.video_label_front = tk.Label(self.video_frame, bg=bg_color)
        self.video_label_front.pack(side="left", padx=10, pady=10)
        self.video_label_side = tk.Label(self.video_frame, bg=bg_color)
        self.video_label_side.pack(side="right", padx=10, pady=10)
        self.cap_front = CameraThread(0) 
        self.cap_side = CameraThread(1) 
        speak_async("Trening rozpoczęty. Pamiętaj o prostej postawie.")
        self.update_video()

    def update_video(self):
        if not self.is_training:
            return

        ret_front, frame_front = self.cap_front.read()
        ret_side, frame_side = self.cap_side.read()
        
        if ret_front and ret_side:
            frame_front = cv2.resize(frame_front, (540, 405))
            frame_side = cv2.resize(frame_side, (540, 405))
            
            self.frame_counter += 1
            if self.last_results_front is None or self.last_results_side is None:
                self.last_results_front = self.pose_model(frame_front, verbose=False)
                self.last_results_side = self.pose_model(frame_side, verbose=False)
            elif self.frame_counter % 2 == 0:
                self.last_results_front = self.pose_model(frame_front, verbose=False)
            else:
                self.last_results_side = self.pose_model(frame_side, verbose=False)
            
            results_side = self.last_results_side
            results_front = self.last_results_front
            
            image_side_rgb = cv2.cvtColor(frame_side, cv2.COLOR_BGR2RGB)
            image_front_rgb = cv2.cvtColor(frame_front, cv2.COLOR_BGR2RGB)

            feedback_front = ""
            feedback_side = ""

            # --- FRONT CAMERA ANALYSIS ---
            if len(results_front) > 0 and results_front[0].keypoints is not None and len(results_front[0].keypoints.xy) > 0:
                keypoints_f = results_front[0].keypoints.xy[0].tolist()
                if len(keypoints_f) > 6 and keypoints_f[5][0] != 0 and keypoints_f[6][0] != 0:
                    left_shoulder_x = keypoints_f[5][0]
                    right_shoulder_x = keypoints_f[6][0]
                    center_x = (left_shoulder_x + right_shoulder_x) / 2
                    
                    frame_w = frame_front.shape[1]
                    if center_x < frame_w * 0.35 or center_x > frame_w * 0.65:
                        feedback_front = "Prosze stanac na srodku"
                    else:
                        if len(keypoints_f) > 10 and (keypoints_f[9][0] == 0 or keypoints_f[10][0] == 0):
                            feedback_front = "Ustaw rece w kadrze"
                else:
                    feedback_front = "Stan w kadrze"
            else:
                feedback_front = "Brak sylwetki"

            if feedback_front:
                image_front_rgb = draw_centered_transparent_text(image_front_rgb, feedback_front, font_scale=0.8, color=(255, 100, 100))

            # --- SIDE CAMERA ANALYSIS ---
            if results_side and len(results_side) > 0 and results_side[0].keypoints is not None and len(results_side[0].keypoints.xy) > 0:
                try:
                    annotated_frame = results_side[0].plot(img=frame_side)
                except Exception:
                    annotated_frame = results_side[0].plot()
                image_side_rgb = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
                
                keypoints = results_side[0].keypoints.xy[0].tolist()
                
                if len(keypoints) > 9 and keypoints[5][0] != 0 and keypoints[7][0] != 0 and keypoints[9][0] != 0:
                    shoulder = [keypoints[5][0], keypoints[5][1]]
                    elbow = [keypoints[7][0], keypoints[7][1]]
                    wrist = [keypoints[9][0], keypoints[9][1]]

                    angle = calculate_angle(shoulder, elbow, wrist)
                    
                    image_side_rgb = draw_centered_transparent_text(image_side_rgb, f"Kat: {int(angle)}", font_scale=0.7, y_offset=-100)

                    if angle > 150:
                        self.stage = "dół"
                        feedback_side = "Reka wyprostowana"
                    elif angle < 40 and self.stage == 'dół':
                        self.stage = "góra"
                        self.rep_count += 1
                        speak_async(f"{self.rep_count}")
                        feedback_side = "Swietnie! (+1)"
                    elif angle < 90 and angle > 50 and self.stage == 'dół':
                        feedback_side = "Dociagnij ruch"
                    elif self.stage == 'góra' and angle > 50 and angle < 140:
                        feedback_side = "Opuszczaj powoli"

                    if feedback_side:
                        image_side_rgb = draw_centered_transparent_text(image_side_rgb, feedback_side, font_scale=0.8, color=(50, 255, 50))
                    
                    self.info_label.configure(text=f"Powtórzenia: {self.rep_count}  |  Technika: {feedback_side if feedback_side else 'W toku'}")

            img_side = Image.fromarray(image_side_rgb)
            imgtk_side = ImageTk.PhotoImage(image=img_side)
            self.video_label_side.imgtk = imgtk_side
            self.video_label_side.configure(image=imgtk_side)
            
            img_front = Image.fromarray(image_front_rgb)
            imgtk_front = ImageTk.PhotoImage(image=img_front)
            self.video_label_front.imgtk = imgtk_front
            self.video_label_front.configure(image=imgtk_front)

        if self.is_training:
            self.after(15, self.update_video)

    def stop_training(self):
        self.is_training = False
        if hasattr(self, 'cap_front') and self.cap_front:
            self.cap_front.release()
        if hasattr(self, 'cap_side') and self.cap_side:
            self.cap_side.release()

        duration = int(time.time() - self.start_time)
        current_date = datetime.datetime.now()

        if self.rep_count > 0:
            try:
                conn = get_db_connection()
                if conn:
                    c = conn.cursor()
                    c.execute(
                        "INSERT INTO workouts (user_id, date, exercise_type, reps, duration_sec) VALUES (?, ?, ?, ?, ?)",
                        (self.current_user_id, current_date, "Biceps", self.rep_count, duration))
                    conn.commit()
                    conn.close()
                    speak_async(f"Świetna robota. Zapisano {self.rep_count} powtórzeń.")
                else:
                    speak_async("Brak połączenia z bazą danych.")
            except Exception as e:
                print(f"Database error: {e}")
                speak_async("Wystąpił błąd podczas zapisu treningu.")
        else:
            speak_async("Trening zakończony.")

        self.show_dashboard_screen()


if __name__ == "__main__":
    app = CyberTrenerApp()
    app.mainloop()