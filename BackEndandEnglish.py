import tkinter as tk
import random
import json
from tkinter import messagebox
from tkinter import colorchooser
from tkinter import font

class AnaUygulama(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Mülakat Uygulaması")
        self.geometry("800x600")

        # Menü Bar
        menubar = tk.Menu(self)
        sayfalar_menu = tk.Menu(menubar, tearoff=0)
        sayfalar_menu.add_command(label="Ana Sayfa", command=self.show_ana_sayfa)
        sayfalar_menu.add_command(label="Back-end", command=self.show_backend_sayfa)
        sayfalar_menu.add_command(label="İngilizce Mülakat", command=self.show_ingilizce_sayfa)
        menubar.add_cascade(label="Sayfalar", menu=sayfalar_menu)
        self.config(menu=menubar)

        self.current_frame = None

    def show_frame(self, frame_class):
        if self.current_frame:
            self.current_frame.pack_forget()

        self.current_frame = frame_class(self)
        self.current_frame.pack(expand=True, fill="both")

    def show_ana_sayfa(self):
        self.show_frame(AnaSayfa)

    def show_backend_sayfa(self):
        self.show_frame(BackendSayfa)

    def show_ingilizce_sayfa(self):
        self.show_frame(IngilizceSayfa)


class AnaSayfa(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg="lightgrey")
        tk.Label(self, text="Ana Sayfa", font=("Arial", 24, "bold"), bg="lightgrey").pack(pady=20)
        tk.Label(self, text="Lütfen üst menüden bir sayfa seçin.", bg="lightgrey").pack(pady=10)

        # Kullanım Klavuzu
        klavuz = """Ana Özellikler:
        - Menü Bar: "Sayfalar" adında bir menü bar, farklı sayfalar arasında geçiş yapmanızı sağlar.
        - Soru Listesi: Her sayfada, mülakat sorularının bir listesi bulunur.
        - Soru Detayları: Listeden bir soru seçildiğinde ya da "Soru Getir" düğmesi tıklandığında, sorunun detayları gösterilir.
        - Not Kaydı: Her soru için notlarınızı kaydedebilirsiniz.

        Nasıl Kullanılır:
        1. Sayfa Seçimi: Menü bardan istediğiniz sayfayı seçin ("Ana Sayfa", "Back-end", "İngilizce Mülakat").
        2. Soru Seçimi: İki yöntemle soru seçebilirsiniz:
            - Listeden bir soru seçin.
            - "Soru Getir" düğmesine tıklayarak rastgele bir soru getirin.
        3. Not Alın: Sağ tarafta bulunan Text Widget'ına notlarınızı girin.
        4. Notu Kaydet: "Notu Kaydet" düğmesine tıklayarak notlarınızı kaydedin.

        Dikkat Edilmesi Gerekenler:
        - Notlar, belirtilen dosya yolunda JSON formatında kaydedilir. Eğer belirtilen yol mevcut değilse, kod çalışmayacaktır.
        - Sorular önceden tanımlıdır. Soru eklemek ya da çıkarmak için kodu manuel olarak değiştirmeniz gerekmektedir."""

        line_count = klavuz.count('\n') + 5

        text_widget = tk.Text(self, wrap=tk.WORD, height=line_count, bg="#F0F0F0", fg="#333")
        text_widget.insert(tk.END, klavuz)
        text_widget.config(state=tk.DISABLED, font=("Arial", 12))
        text_widget.pack(pady=20)
        
class BackendSayfa(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg="lightgrey")
        tk.Label(self, text="Back-end Mülakat", font=("Arial", 12, "bold"), bg="lightgrey").pack(pady=16)
        self.color_dict = self.load_colors()
        self.label_frames = []
        self.sorular = [
            {
                "soru": "Hangi programlama dillerini biliyorsunuz ve hangisinde en rahat hissediyorsunuz?",
                "anahtar_kelimeler": "Temel Programlama"
            },
            {
                "soru": "Nesne yönelimli programlama nedir? Bir örnek ile açıklayabilir misiniz?",
                "anahtar_kelimeler": "skills, abilities, achievements, examples"
            },
            {
                "soru": "Rekürsif bir fonksiyon nedir ve ne zaman kullanılır?",
                "anahtar_kelimeler": "self-awareness, improvement, steps, progress"
            },
            {
                "soru": "Asenkron programlama hakkında ne biliyorsunuz?",
                "anahtar_kelimeler": "company values, culture, growth, opportunities"
            },
            {
                "soru": "SQL ve NoSQL arasındaki temel farklar nelerdir?",
                "anahtar_kelimeler": "short-term, long-term, aspirations, development"
            },
            {
                "soru": "Bir SQL sorgusu yazarak bir tablodan belirli verileri çekmek için bir örnek gösterebilir misiniz?",
                "anahtar_kelimeler": "unique qualities, value, contributions, fit"
            },
            {
                "soru": "Veritabanı normalizasyonu nedir?",
                "anahtar_kelimeler": "stress management, coping mechanisms, examples"
            },
            {
                "soru": "ACID prensipleri nelerdir?",
                "anahtar_kelimeler": "achievement, impact, skills demonstrated, story"
            },
            {
                "soru": "RESTful API nedir?",
                "anahtar_kelimeler": "challenge, actions, result, lessons learned"
            },
            {
                "soru": "HTTP ve HTTPS arasındaki farklar nelerdir?",
                "anahtar_kelimeler": "company culture, growth, expectations, team"
            },
            {
                "soru": "Bir sunucu nasıl ölçeklenir?",
                "anahtar_kelimeler": "acceptance, learning, resilience, example"
            },
            {
                "soru": "Bir mikrohizmet mimarisi nedir ve ne avantajları vardır?",
                "anahtar_kelimeler": "inspiration, goals, achievements, growth"
            },
            {
                "soru": "Versiyon kontrol sistemleri hakkında ne biliyorsunuz? Git ile daha önce çalıştınız mı?",
                "anahtar_kelimeler": "culture, team, management style, work-life balance"
            },
            {
                "soru": "DevOps hakkında ne düşünüyorsunuz? CI/CD pipeline nedir?",
                "anahtar_kelimeler": "time management, deadlines, importance, strategy"
            },
            {
                "soru": "Test Driven Development (TDD) nedir ve avantajları nelerdir?",
                "anahtar_kelimeler": "research, market value, experience, negotiation"
            },
            {
                "soru": "Temel bir algoritma sorusu (örneğin, bir dizi sıralama veya bir ağaçta arama yapma).",
                "anahtar_kelimeler": "conflict resolution, communication, understanding, result"
            },
            {
                "soru": "Big O  gösterimi nedir? Örneklerle açıklayabilir misiniz?",
                "anahtar_kelimeler": "impact, recognition, skillset, example"
            },
            {
                "soru": "Hash tablosu ve onun avantajları nelerdir?",
                "anahtar_kelimeler": "resources, networking, conferences, continuous learning"
            },
            {
                "soru": "Sıralı ve sırasız listeler arasındaki farklar nelerdir?",
                "anahtar_kelimeler": "prioritization, time management, focus, communication"
            },
            {
                "soru": "Bellek yönetimi hakkında ne biliyorsunuz?",
                "anahtar_kelimeler": "empathy, listening, problem-solving, outcome"
            },
            {
                "soru": "Bir veritabanında indeksleme ne işe yarar?",
                "anahtar_kelimeler": "team, collaboration, structure, flexibility"
            },
            {
                "soru": "CAP teoremi nedir?",
                "anahtar_kelimeler": "planning, tools, prioritization, routine"
            },
            {
                "soru": "Redis gibi anahtar-değer depolama sistemlerinin tipik kullanım senaryoları nelerdir?",
                "anahtar_kelimeler": "adaptability, resourcefulness, learning, example"
            },
            {
                "soru": "Bir ORM (Object-Relational Mapping) nedir ve neden kullanılır?",
                "anahtar_kelimeler": "analysis, intuition, collaboration, confidence"
            },
            {
                "soru": "CORS (Cross-Origin Resource Sharing) nedir?",
                "anahtar_kelimeler": "clarity, active listening, adaptability, examples"
            },
            {
                "soru": "Websocket nedir?",
                "anahtar_kelimeler": "influence, negotiation, logic, example"
            },
            {
                "soru": "GraphQL'in REST'ten farkı nedir?",
                "anahtar_kelimeler": "vision, motivation, delegation, adaptability"
            },
            {
                "soru": "Server-side rendering ve client-side rendering arasındaki farklar nelerdir?",
                "anahtar_kelimeler": "flexibility, adaptability, learning, resilience"
            },
            {
                "soru": "Docker'ı tanımlayabilir misiniz?",
                "anahtar_kelimeler": "passions, balance, personal growth, networking"
            },
            {
                "soru": "Bir yük dengeleyici (Load Balancer) ne işe yarar?",
                "anahtar_kelimeler": "critical thinking, creativity, collaboration, example"
            },
            {
                "soru": "Bir API Gateway nedir?",
                "anahtar_kelimeler": "collaboration, communication, support, example"
            },
            {
                "soru": "Serverless mimari nedir?",
                "anahtar_kelimeler": "openness, learning, improvement, example"
            },
            {
                "soru": "MVC (Model-View-Controller) mimarisi nedir?",
                "anahtar_kelimeler": "proactivity, creativity, impact, example"
            },
            {
                "soru": "Singleton tasarım örüntüsü nedir ve ne zaman kullanılır?",
                "anahtar_kelimeler": "tools, communication, discipline, adaptability"
            },
            {
                "soru": "Clean Code (Temiz Kod) hakkında ne düşünüyorsunuz?",
                "anahtar_kelimeler": "research, collaboration, resourcefulness, learning"
            },
            {
                "soru": "Monolitik ve mikrohizmetler mimarisi arasındaki temel farklar nelerdir?",
                "anahtar_kelimeler": "attention to detail, standards, review, example"
            },
            {
                "soru": "JIRA, Trello gibi proje yönetim araçları hakkında deneyiminiz var mı?",
                "anahtar_kelimeler": "time management, prioritization, organization, example"
            },
            {
                "soru": "Code Review'un önemi nedir?",
                "anahtar_kelimeler": "goals, focus, variation, personal strategies"
            },
            {
                "soru": "Bir pull request ne zaman kabul edilmemelidir?",
                "anahtar_kelimeler": "boundaries, hobbies, self-care, time management"
            },
            {
                "soru": "Agile ve Scrum metodolojileri hakkında ne biliyorsunuz?",
                "anahtar_kelimeler": "diversity, empathy, active listening, example"
            },
            {
                "soru": "SQL enjeksiyonu nedir ve nasıl önlenir?",
                "anahtar_kelimeler": "culture, teamwork, growth, work-life balance"
            },
            {
                "soru": "XSS (Cross-Site Scripting) saldırıları nedir?",
                "anahtar_kelimeler": "time management, prioritization, teamwork, example"
            },
            {
                "soru": "Kimlik doğrulama ve yetkilendirme arasındaki fark nedir?",
                "anahtar_kelimeler": "professional development, resources, curiosity, goals"
            },
            {
                "soru": "JWT (JSON Web Token) nedir ve ne için kullanılır?",
                "anahtar_kelimeler": "time management, organization, goals, environment"
            },
            {
                "soru": "Birim testi nedir ve neden önemlidir?",
                "anahtar_kelimeler": "communication, empathy, resolution, example"
            },
            {
                "soru": "TDD (Test Driven Development) hakkında ne düşünüyorsunuz?",
                "anahtar_kelimeler": "organization, prioritization, communication, example"
            },
            {
                "soru": "Loglama nedir ve neden önemlidir?",
                "anahtar_kelimeler": "vision, motivation, adaptability, communication"
            },
            {
                "soru": "Bir hata ayıklama sürecinde genellikle hangi adımları takip edersiniz?",
                "anahtar_kelimeler": "adaptability, problem-solving, resilience, example"
            },
            {
                "soru": "Git'in temel komutları nelerdir?",
                "anahtar_kelimeler": "initiative, dedication, impact, example"
            },
            {
                "soru": "CI/CD (Continuous Integration/Continuous Deployment) nedir?",
                "anahtar_kelimeler": "communication, trust, collaboration, support"
            },
            {
                "soru": "Postman veya benzeri API test araçları hakkında deneyiminiz var mı?",
                "anahtar_kelimeler": "communication, trust, collaboration, support"
            },
            {
                "soru": "Bir IDE'nin (Entegre Geliştirme Ortamı) temel avantajları ve dezavantajları nelerdir?",
                "anahtar_kelimeler": "communication, trust, collaboration, support"
            },
            {
                "soru": "Python'da asenkron programlama nasıl yapılır?",
                "anahtar_kelimeler": "communication, trust, collaboration, support"
            },
            {
                "soru": "Java'da garbage collector'ın işleyişi nasıldır?",
                "anahtar_kelimeler": "communication, trust, collaboration, support"
            },
            {
                "soru": "Node.js event loop mekanizması nedir?",
                "anahtar_kelimeler": "communication, trust, collaboration, support"
            },
            {
                "soru": ".NET Core ve .NET Framework arasındaki temel farklar nelerdir?",
                "anahtar_kelimeler": "communication, trust, collaboration, support"
            },
            {
                "soru": "SOLID ilkeleri nelerdir ve neden önemlidir?",
                "anahtar_kelimeler": "communication, trust, collaboration, support"
            },
            {
                "soru": "DRY (Don't Repeat Yourself) ve YAGNI (You Aren't Gonna Need It) ilkelerini açıklayabilir misiniz?",
                "anahtar_kelimeler": "communication, trust, collaboration, support"
            },
            {
                "soru": "Coupling ve Cohesion arasındaki fark nedir?",
                "anahtar_kelimeler": "communication, trust, collaboration, support"
            },
            {
                "soru": "N-Tier ve N-Layer mimarileri arasında ne gibi farklar vardır?",
                "anahtar_kelimeler": "communication, trust, collaboration, support"
            },
            {
                "soru": "Şu ana kadar üzerinde çalıştığınız en karmaşık proje nedir?",
                "anahtar_kelimeler": "communication, trust, collaboration, support"
            },
            {
                "soru": "Hangi proje yönetim metodolojileriyle deneyiminiz var?",
                "anahtar_kelimeler": "communication, trust, collaboration, support"
            },
            {
                "soru": "Yazılım geliştirme sürecinde karşılaştığınız en büyük zorluklar nelerdir?",
                "anahtar_kelimeler": "communication, trust, collaboration, support"
            },
            {
                "soru": "Açık kaynak projelerine katkıda bulundunuz mu? Eğer evetse, hangi projeler?",
                "anahtar_kelimeler": "communication, trust, collaboration, support"
            }
        ]

        self.init_ui()
        self.load_notes()


    def init_ui(self):
        self.canvas = tk.Canvas(self, bg="lightgrey")
        scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="lightgrey")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        for index, soru in enumerate(self.sorular):
            color = self.color_dict.get(soru["soru"], "white")
            label_frame = tk.Frame(self.scrollable_frame, bg=color)
            label_frame.pack(fill="x")
            label = tk.Label(label_frame, text=soru["soru"], bg=color)
            label.pack(side="left", fill="x", expand=True)
            label.bind("<Button-1>", lambda event, s=soru: self.label_click(event, s))
            self.label_frames.append(label_frame)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="left", fill="y")
        self.left_frame = tk.Frame(self, bg="lightgrey")
        self.left_frame.pack(side="left", fill="both", padx=10, pady=10, expand=1)

        self.right_frame = tk.Frame(self, bg="lightgrey")
        self.right_frame.pack(side="right", fill="both", padx=10, pady=10,expand=1)

        self.soru_label = tk.Label(self.right_frame, text="", wraplength=400, bg="lightgrey")
        self.soru_label.pack(pady=10)

        self.not_entry = tk.Text(self.right_frame, width=70, height=25)
        self.not_entry.pack(pady=10)

        self.kaydet_button = tk.Button(self.right_frame, text="Notu Kaydet", command=self.save_note)
        self.kaydet_button.pack(pady=10)

        self.getir_button = tk.Button(self.right_frame, text="Soru Getir", command=self.get_random_soru)
        self.getir_button.pack(pady=10)
        
        self.tamamla_button = tk.Button(self.right_frame, text="Soruyu Tamamla", command=self.complete_question)
        self.tamamla_button.pack(pady=10)
        
        # for index, soru in enumerate(self.sorular):
        #     color = self.color_dict.get(soru["soru"], "white")
        #     label_frame = tk.Frame(self.left_frame, bg=color)
        #     label_frame.pack(fill="x")
        #     label = tk.Label(label_frame, text=soru["soru"], bg=color)
        #     label.pack(side="left", fill="x", expand=True)
        #     label.bind("<Button-1>", lambda event, s=soru: self.label_click(event, s))
        #     self.label_frames.append(label_frame)
    def label_click(self, event, soru):
        try:
            self.show_soru(soru)
            event.widget.master.config(bg="blue")  # Anlık olarak mavi yapılıyor
        except:
            pass
    def complete_question(self):
        selected_soru = self.current_soru
        self.color_dict[selected_soru["soru"]] = "green"
        self.save_colors(self.color_dict)
        self.update_label_color(selected_soru, "green")

    def load_notes(self):
        try:
            with open("backendnotes.json", "r") as file:
                self.notes = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.notes = {}
    # Renkleri kaydet
    def save_colors(self, color_dict):  # self parametresi eklendi
        with open("colors.json", "w") as f:
            json.dump(color_dict, f)

    # Renkleri yükle
    def load_colors(self):
        try:
            with open("colors.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    def show_main_frame(self):
        self.right_frame.pack(side="right", fill="both", expand=True)

    def save_notes(self):
        with open("backendnotes.json", "w") as file:

            json.dump(self.notes, file)

    def get_random_soru(self):
        soru = random.choice(self.sorular)
        self.show_soru(soru)

    def listbox_click(self, event, soru):
        selected = self.listbox.curselection()
        if selected:
            index = selected[0]
        index = self.listbox.curselection()[0]
        soru = self.sorular[index]
        self.show_soru(soru)

    def show_soru(self, soru):
        self.current_soru = soru
        self.soru_label.config(text=soru["soru"])
        note_data = self.notes.get(soru["soru"], {"note": ""})
        self.not_entry.delete(1.0, "end")
        self.not_entry.insert(1.0, note_data.get("note", ""))
    def save_note(self):
        not_text = self.not_entry.get(1.0, "end-1c")
        self.notes[self.current_soru["soru"]] = {"note": not_text}
        self.color_dict[self.current_soru["soru"]] = "orange"
        self.save_colors(self.color_dict)
        self.update_label_color(self.current_soru, "orange")
        self.save_notes()
        messagebox.showinfo("Bilgi", "Not başarıyla kaydedildi!")
    def update_label_color(self, soru, color):
        for label_frame in self.label_frames:
            label = label_frame.winfo_children()[0]
            if label.cget("text") == soru["soru"]:
                label_frame.config(bg=color)
                label.config(bg=color)
                break
    def show_other_frame(self):
        other_frame = tk.Toplevel(self)
        other_frame.geometry("600x400")
        tk.Label(other_frame, text="Diğer Sayfa").pack()
        tk.Button(other_frame, text="Geri Dön", command=other_frame.destroy).pack()
class IngilizceSayfa(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        tk.Label(self, text="İngilizce Mülakat", font=('Helvetica', 16)).pack(pady=10)

        self.sorular = [
            {
                "soru": "Tell me about yourself.",
                "anahtar_kelimeler": "background, education, experience, skills"
            },
            {
                "soru": "What are your strengths?",
                "anahtar_kelimeler": "skills, abilities, achievements, examples"
            },
            {
                "soru": "What are your weaknesses?",
                "anahtar_kelimeler": "self-awareness, improvement, steps, progress"
            },
            {
                "soru": "Why do you want to work for our company?",
                "anahtar_kelimeler": "company values, culture, growth, opportunities"
            },
            {
                "soru": "What are your career goals?",
                "anahtar_kelimeler": "short-term, long-term, aspirations, development"
            },
            {
                "soru": "Why should we hire you?",
                "anahtar_kelimeler": "unique qualities, value, contributions, fit"
            },
            {
                "soru": "How do you handle stress and pressure?",
                "anahtar_kelimeler": "stress management, coping mechanisms, examples"
            },
            {
                "soru": "What is your greatest accomplishment?",
                "anahtar_kelimeler": "achievement, impact, skills demonstrated, story"
            },
            {
                "soru": "Describe a difficult work situation and how you overcame it.",
                "anahtar_kelimeler": "challenge, actions, result, lessons learned"
            },
            {
                "soru": "Do you have any questions for us?",
                "anahtar_kelimeler": "company culture, growth, expectations, team"
            },
            {
                "soru": "How do you handle failure?",
                "anahtar_kelimeler": "acceptance, learning, resilience, example"
            },
            {
                "soru": "What motivates you?",
                "anahtar_kelimeler": "inspiration, goals, achievements, growth"
            },
            {
                "soru": "What is your ideal work environment?",
                "anahtar_kelimeler": "culture, team, management style, work-life balance"
            },
            {
                "soru": "How do you prioritize tasks?",
                "anahtar_kelimeler": "time management, deadlines, importance, strategy"
            },
            {
                "soru": "What are your salary expectations?",
                "anahtar_kelimeler": "research, market value, experience, negotiation"
            },
            {
                "soru": "Describe a time when you had to work with a difficult team member.",
                "anahtar_kelimeler": "conflict resolution, communication, understanding, result"
            },
            {
                "soru": "What do you consider to be your greatest professional achievement?",
                "anahtar_kelimeler": "impact, recognition, skillset, example"
            },
            {
                "soru": "How do you stay updated on industry trends and developments?",
                "anahtar_kelimeler": "resources, networking, conferences, continuous learning"
            },
            {
                "soru": "How do you handle tight deadlines?",
                "anahtar_kelimeler": "prioritization, time management, focus, communication"
            },
            {
                "soru": "Describe a time when you had to deal with an unhappy customer or client.",
                "anahtar_kelimeler": "empathy, listening, problem-solving, outcome"
            },
            {
                "soru": "What type of work environment do you prefer?",
                "anahtar_kelimeler": "team, collaboration, structure, flexibility"
            },
            {
                "soru": "How do you stay organized?",
                "anahtar_kelimeler": "planning, tools, prioritization, routine"
            },
            {
                "soru": "Tell me about a time you had to learn something new quickly.",
                "anahtar_kelimeler": "adaptability, resourcefulness, learning, example"
            },
            {
                "soru": "How do you make decisions?",
                "anahtar_kelimeler": "analysis, intuition, collaboration, confidence"
            },
            {
                "soru": "Describe your communication style.",
                "anahtar_kelimeler": "clarity, active listening, adaptability, examples"
            },
            {
                "soru": "Tell me about a time you had to persuade someone.",
                "anahtar_kelimeler": "influence, negotiation, logic, example"
            },
            {
                "soru": "What is your leadership style?",
                "anahtar_kelimeler": "vision, motivation, delegation, adaptability"
            },
            {
                "soru": "How do you deal with change?",
                "anahtar_kelimeler": "flexibility, adaptability, learning, resilience"
            },
            {
                "soru": "What are your hobbies and interests outside of work?",
                "anahtar_kelimeler": "passions, balance, personal growth, networking"
            },
            {
                "soru": "What is your approach to problem-solving?",
                "anahtar_kelimeler": "critical thinking, creativity, collaboration, example"
            },
            {
                "soru": "How do you approach teamwork?",
                "anahtar_kelimeler": "collaboration, communication, support, example"
            },
            {
                "soru": "How do you handle criticism or feedback?",
                "anahtar_kelimeler": "openness, learning, improvement, example"
            },
            {
                "soru": "Tell me about a time you demonstrated initiative.",
                "anahtar_kelimeler": "proactivity, creativity, impact, example"
            },
            {
                "soru": "What experience do you have working remotely?",
                "anahtar_kelimeler": "tools, communication, discipline, adaptability"
            },
            {
                "soru": "What do you do when you don't know the answer to a problem?",
                "anahtar_kelimeler": "research, collaboration, resourcefulness, learning"
            },
            {
                "soru": "How do you ensure the quality of your work?",
                "anahtar_kelimeler": "attention to detail, standards, review, example"
            },
            {
                "soru": "Tell me about a time when you had to juggle multiple priorities.",
                "anahtar_kelimeler": "time management, prioritization, organization, example"
            },
            {
                "soru": "How do you stay motivated during repetitive tasks?",
                "anahtar_kelimeler": "goals, focus, variation, personal strategies"
            },
            {
                "soru": "What steps do you take to maintain a healthy work-life balance?",
                "anahtar_kelimeler": "boundaries, hobbies, self-care, time management"
            },
            {
                "soru": "Tell me about a time when you had to adapt your communication style.",
                "anahtar_kelimeler": "diversity, empathy, active listening, example"
            },
            {
                "soru": "What do you value most in a workplace?",
                "anahtar_kelimeler": "culture, teamwork, growth, work-life balance"
            },
            {
                "soru": "Tell me about a time when you had to deal with a challenging deadline.",
                "anahtar_kelimeler": "time management, prioritization, teamwork, example"
            },
            {
                "soru": "How do you continue learning and growing in your field?",
                "anahtar_kelimeler": "professional development, resources, curiosity, goals"
            },
            {
                "soru": "What strategies do you use to stay focused and productive?",
                "anahtar_kelimeler": "time management, organization, goals, environment"
            },
            {
                "soru": "How do you handle conflicts with colleagues?",
                "anahtar_kelimeler": "communication, empathy, resolution, example"
            },
            {
                "soru": "Tell me about a time when you had to manage multiple projects at once.",
                "anahtar_kelimeler": "organization, prioritization, communication, example"
            },
            {
                "soru": "What do you believe makes a great leader?",
                "anahtar_kelimeler": "vision, motivation, adaptability, communication"
            },
            {
                "soru": "How do you handle unexpected obstacles or challenges?",
                "anahtar_kelimeler": "adaptability, problem-solving, resilience, example"
            },
            {
                "soru": "Tell me about a time you went above and beyond for a project or task.",
                "anahtar_kelimeler": "initiative, dedication, impact, example"
            },
            {
                "soru": "How do you build relationships with team members and colleagues?",
                "anahtar_kelimeler": "communication, trust, collaboration, support"
            }
        ]

        self.favoriler = set()
        self.init_ui()
        self.load_notes()

    def init_ui(self):

        self.listbox = tk.Listbox(self, selectmode="single", width=50, height=20, font=('Helvetica', 12))
        self.listbox.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        self.right_frame = tk.Frame(self, bg='grey')
        self.right_frame.pack(side="right", fill="both", expand=True)

        self.soru_label = tk.Label(self.right_frame, text="", wraplength=400, font=('Helvetica', 14), bg='grey')
        self.soru_label.pack(pady=10)

        self.anahtar_label = tk.Label(self.right_frame, text="", wraplength=400, font=('Helvetica', 12), fg='black', bg='grey')
        self.anahtar_label.pack(pady=5)

        self.not_entry = tk.Text(self.right_frame, width=50, height=20, font=('Helvetica', 12))
        self.not_entry.pack(pady=10, padx=10)

        self.kaydet_button = tk.Button(self.right_frame, text="Notu Kaydet", command=self.save_note)
        self.kaydet_button.pack(pady=10)

        self.getir_button = tk.Button(self.right_frame, text="Soru Getir", command=self.get_random_soru)
        self.getir_button.pack(pady=10)
        for index, soru in enumerate(self.sorular):
            self.listbox.insert(index, soru["soru"])

        self.listbox.bind("<<ListboxSelect>>", self.listbox_click)

    def load_notes(self):
        try:
            with open("ingilizcenotes.json", "r") as file:

                self.notes = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.notes = {}
    def show_main_frame(self):
        self.right_frame.pack(side="right", fill="both", expand=True)

    def save_notes(self):
        with open("ingilizcenotes.json", "w") as file:

            json.dump(self.notes, file)

    def get_random_soru(self):
        soru = random.choice(self.sorular)
        self.show_soru(soru)

    def listbox_click(self, event):
        index = self.listbox.curselection()[0]
        soru = self.sorular[index]
        self.show_soru(soru)

    def show_soru(self, soru):
        self.current_soru = soru
        self.soru_label.config(text=soru["soru"])
        self.anahtar_label.config(text=f"Anahtar Kelimeler: {soru['anahtar_kelimeler']}")

        note_data = self.notes.get(soru["soru"], "keywords" "")

        self.not_entry.delete(1.0, "end")
        self.not_entry.insert(1.0, note_data.get("note", ""))



    def save_note(self):
        not_text = self.not_entry.get(1.0, "end-1c")
        
        self.notes[self.current_soru["soru"]] = {
            "note": not_text,
        }
        
        self.save_notes()
        messagebox.showinfo("Bilgi", "Not başarıyla kaydedildi!")
    def show_other_frame(self):
        other_frame = tk.Toplevel(self)
        other_frame.geometry("600x400")
        tk.Label(other_frame, text="Diğer Sayfa").pack()
        tk.Button(other_frame, text="Geri Dön", command=other_frame.destroy).pack()


if __name__ == "__main__":
    app = AnaUygulama()
    app.show_ana_sayfa()
    app.mainloop()
