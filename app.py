import streamlit as st
import pandas as pd
import io
from sklearn.preprocessing import MinMaxScaler
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

veri_sozlugu = {
    "1.1. Bilimsel Yayın Sayısı": "2022 yılında ISI Citation Index (SCI, SCI-E, SSCI ve A&HCI) veri tabanında taranan dergilerdeki makale (article) ve derleme (review) türündeki yayın sayısı.",
    "1.2. Atıf Sayısı": "ISI Citation Index (SCI, SCI-E, SSCI ve A&HCI) veri tabanında taranan dergilerde 2017-2022 yıllarını kapsayan dönemde yayınlanan tüm makale ve derlemelere yapılan toplam atıf sayısı.",
    "1.3. Ulusal Ar-Ge ve Yenilik Destek Programlarından Alınan Proje Sayısı": "Ulusal Ar-Ge ve Yenilik Destek Programları tarafından desteklenen, 2022 yılında başlamış, devam eden veya tamamlanmış proje sayısı.",
    "1.4. Ulusal Ar-Ge ve Yenilik Destek Programlarından Kuruma Aktarılan Fon Tutarı": "Ulusal Ar-Ge ve Yenilik Destek Programları tarafından desteklenen projeler kapsamında 2022 yılında kuruma aktarılan toplam bütçe tutarı.",
    "1.5. Uluslararası Proje Fon Tutarı": "HORIZON 2020, İkili ve Çoklu İşbirlikleri, COST, ERA-NET gibi Uluslararası Destek Programları tarafından desteklenen projeler için 2022 yılında kuruma aktarılan toplam bütçe tutarı.",
    "1.6. Ulusal ve Uluslararası Patent Başvuru Sayısı": "Son 3 yılda (2020-2022) Türk Patent ve Marka Kurumu'na yapılan ulusal ve uluslararası patent başvuru sayısı.",
    "1.7. Ulusal Patent Belge Sayısı": "Son 3 yılda (2020-2022) Türk Patent ve Marka Kurumu tarafından tescillenmiş ulusal patent sayısı.",
    "1.8. Uluslararası Patent Belge Sayısı": "Son 3 yılda (2020-2022) yurtdışı patent ofisleri tarafından tescillenmiş uluslararası patent sayısı.",
    "1.9. Faydalı Model ve Tasarım Belge Sayısı": "Son 3 yılda (2020-2022) Türk Patent ve Marka Kurumu tarafından tescillenmiş faydalı model ve tasarım sayısı.",
    "1.10. Ufuk Avrupa Proje Başvuru Sayısı": "Ufuk Avrupa 2022 yılı çağrıları kapsamında kurum veya kurum mensupları tarafından başvuru yapılan proje sayısı.",
    "1.11. Ufuk Avrupa Kabul Edilen Proje Sayısı": "Ufuk Avrupa 2022 yılı çağrıları kapsamında TÜBİTAK tarafından kabul edilen proje sayısı.",
    "2.1. Incites Dergi Etki Değerinde ilk %50’lik Dilime Giren Bilimsel Yayın Oranı": "2022 yılında Incites Dergi Etki Değerinde ilk %50’lik dilime giren (Q1+Q2) makale ve derleme türlerindeki yayınların sayısının aynı yıldaki toplam yayın sayısına oranı.",
    "2.2. %10’luk Dilimde Atıf Alan Yayın Oranı": "2022 yılında ISI Citation Index veri tabanlarında taranan dergilerde yayınlanan ve %10’luk dilimde atıf alan makale ve derleme türlerindeki yayınların oranı.",
    "2.3. Bilim Ödülü Sayısı": "2022 yılında kurum mensuplarının veya öğrencilerin aldığı YÖK, TÜBİTAK, TÜBA GEBİP ödülleri.",
    "2.4. TÜBİTAK 1004 Programı Kapsamında Alınan Fon Tutarı": "TÜBİTAK 1004 Programı kapsamında 2022 yılında kuruma aktarılan fon tutarı.",
    "2.5. Yayınların Açık Erişim Yüzdesi": "2022 yılında ISI Citation Index veri tabanında taranan dergilerdeki yayınların açık erişim oranı.",
    "2.6. Dünya Akademik Sıralamalarındaki Performansı": "2022 yılında THE, QS, ARWU Dünya Akademik Genel Sıralamalarındaki yeri.",
    "2.7. Akredite Edilmiş Program Sayısı": "2022 Yükseköğretim Programları ve Kontenjanları Kılavuzu'na göre akredite edilmiş toplam program sayısı.",
    "2.8. Uluslararası Doktora Öğrenci Oranı": "2021-2022 öğretim yılında öğrenim gören yabancı uyruklu doktora öğrenci oranı.",
    "2.9. Doktora Mezun Sayısı": "2021-2022 öğretim yılında mezun olan doktora öğrenci sayısı.",
    "2.10. Doktora Öğrenci Sayısı": "2021-2022 öğretim yılı doktora öğrenci sayısı.",
    "3.1. Üniversite-Üniversite İşbirlikli Yayın Oranı": "2022 yılında ISI Citation Index veri tabanında taranan dergilerde yayınlanan üniversite-üniversite işbirlikli yayınların oranı.",
    "3.2. Üniversite-İş Dünyası İşbirlikli Yayın Oranı": "2022 yılında ISI Citation Index veri tabanında taranan dergilerde yayınlanan üniversite-iş dünyası işbirlikli yayınların oranı.",
    "3.3. Uluslararası İşbirlikli Yayın Oranı": "2022 yılında ISI Citation Index veri tabanında taranan dergilerde yayınlanan uluslararası işbirlikli yayınların oranı.",
    "3.4. Üniversite-İş Dünyası İşbirlikli Ulusal ve Uluslararası Patent Belge Sayısı": "Son 3 yılda tescillenmiş üniversite-iş dünyası işbirlikli ulusal ve uluslararası patent belge sayısı.",
    "3.5. Uluslararası İşbirlikli Ulusal ve Uluslararası Patent Belge Sayısı": "Son 3 yılda tescillenmiş uluslararası işbirlikli ulusal ve uluslararası patent belge sayısı.",
    "3.6. Kamu Fonları Kapsamında Üniversite-İş Dünyası İşbirliği ile Yapılan Ar-Ge ve Yenilik Projelerinden Alınan Fon Tutarı": "Kamu fonları kapsamında 2022 yılında kuruma aktarılan fon tutarı.",
    "3.7. Kamu Fonları Kapsamında Üniversite – İş Dünyası İş birliği ile Yapılan Ar-Ge ve Yenilik Projeleri Sayısı": "Ulusal Ar-Ge ve Yenilik  Destek Programları tarafından desteklenen, 2022 yılında başlayan, devam eden ya da tamamlanan üniversite-iş dünyası iş birlikli proje sayısı (Ar-Ge ve yenilik alanında fon sağlayan kamu kuruluşları tarafından desteklenen projeler ile kamu destekli iş birliği projelerine sağlanan danışmanlık hizmetleri dahildir. Yatırım projeleri ve BAP projeleri hariçtir.) ",
    "3.8. Uluslararası Öğrenci Oranı" : "Kurumun lisans, yüksek lisans ve doktora programlarında 2021-2022 öğretim yılında öğrenim gören yabancı uyruklu öğrenci sayısının toplam öğrenci sayısına oranı",
    "3.9. Uluslararası Öğretim Üyesi Oranı" : "Kurumda 2021-2022 öğretim yılında Yabancı Diller Yüksek Okulu'ndaki görevlendirmeler dışında görevli yabancı uyruklu öğretim üyesi (Profesör, Doçent, Dr. Öğr. Üyesi) sayısının toplam öğretim üyesi sayısına oranı",
    "3.10. Dolaşımdaki Öğretim Üyesi ve Öğrenci Sayısı" : "2022 yılında, Ulusal Ajans ve TÜBİTAK dolaşım programları kapsamında dolaşımda olan  kurum mensupları ve öğrenci sayısı (gelen ve giden ayrımında)",
    "3.11. TÜBİTAK 2244 Sanayi Doktora Programı Öğrenci" : "2022 yılında TÜBİTAK 2244 Sanayi Doktora Programı'ndan yararlanan kayıtlı toplam öğrenci sayısı"


}



birim_sifreleri = {
    "Kütüphane Daire Başkanlığı" : "",
    "Öğrenci İşleri": "sifre1",
    "BAP": "sifre2",
    "TTO": "sifre3",
    "PDO": "sifre4"
}

def birim_ismini_al(sifre):
    return birim_sifreleri.get(sifre, None)

smtp_server = "smtp.gmail.com"
smtp_port = 587

sender_email = "umitcaninozu@gmail.com"
sender_password = "hodt sryq ekqs riai"

def send_email(recipient_email, subject, body, attachment):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    
    msg.attach(MIMEText(body, 'plain'))
    
    part = MIMEApplication(attachment, Name="kriter_verileri.xlsx")
    part['Content-Disposition'] = 'attachment; filename="kriter_verileri.xlsx"'
    msg.attach(part)
    
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  
            server.login(sender_email, sender_password) 
            server.send_message(msg)
            print(f"Email sent to {recipient_email}")
        
        print("SMTP server connection closed.")
    
    except Exception as e:
        print(f"Error sending email to {recipient_email}: {e}")

if 'sayfa' not in st.session_state:
    st.session_state.sayfa = 1

if 'form_gonderildi' not in st.session_state:
    st.session_state.form_gonderildi = False

def ileri():
    st.session_state.sayfa += 1

def geri():
    st.session_state.sayfa -= 1

if st.session_state.sayfa == 1:
    st.title("Birim Seçimi Ekranı")
    
    # Birim seçimi
    birim_secimi = st.selectbox("Lütfen bir birim seçin", list(birim_sifreleri.keys()))
    
    # Şifre girişi
    sifre = st.text_input("Seçtiğiniz birim için şifreyi girin", type="password")
    
    secilen_kriter = st.selectbox("Veri Sözlüğü İçin Bir Kriter Seçin", list(veri_sozlugu.keys()))

 
    # Seçilen kriterin tanımını gösterin
    if secilen_kriter:
        st.write(f"**{secilen_kriter} Tanımı:**")
        st.write(veri_sozlugu[secilen_kriter])


    
    if st.button("İleri"):
        # Şifre kontrolü
        if sifre == birim_sifreleri.get(birim_secimi):
            st.session_state.fakulte_ismi = birim_secimi
            ileri()  # Şifre doğruysa sonraki sayfaya geçiş
        else:
            st.write("Geçersiz şifre. Lütfen tekrar deneyin.")
            
            


elif st.session_state.sayfa == 2:
    st.title("Veriyi Giren Kullanıcının Bilgileri")
    st.write(f"Birim: {st.session_state.fakulte_ismi}")
    
    unvanlar = ["İdari Personel","Akademik Personel"]
    unvan = st.selectbox("Göreviniz", unvanlar)
    
    ad = st.text_input("Adınız")
    soyad = st.text_input("Soyadınız")
    

    if st.button("Geri"):
        geri()
    if st.button("İleri"):
        if ad and soyad:
            st.session_state.ad = ad
            st.session_state.soyad = soyad
            st.session_state.unvan = unvan

            ileri()
        else:
            st.write("Lütfen adınızı ve soyadınızı girin.")


elif st.session_state.sayfa == 3:
    st.title("Gösterge Giriş Ekranı")
    st.write(f"Birim: {st.session_state.fakulte_ismi}")
    st.write(f"Kullanıcı: {st.session_state.unvan} {st.session_state.ad} {st.session_state.soyad}")
    
    st.write("Lütfen aşağıdaki bilgileri doldurun:")
    
    st.write("Bilgilendirme : Girilmeyen her değer 0 olarak kabul edilecektir.")
    
    
    data = {}
    
    if 'form_tamamlandi' not in st.session_state:
        st.session_state.form_tamamlandi = False

    # Fakülte ismine göre farklı formlar
    if st.session_state.fakulte_ismi == "Öğrenci İşleri":
        ulusal_proje_sayisi = st.text_input("1.3. Ulusal Proje Sayısı  Verisi Girin", value="0")
        if st.button("Tamamla"):
            data = {
                "1.3. Ulusal Proje Sayısı ": ulusal_proje_sayisi
            }
            st.session_state.df = pd.DataFrame([data])
            st.session_state.form_tamamlandi = True


    
    elif st.session_state.fakulte_ismi == "Kütüphane Daire Başkanlığı":
        bilimsel_yayin_sayisi = st.text_input("1.1. Bilimsel Yayın Sayısı Verisi Girin", value="0")
        atif_sayisi = st.text_input("1.2. Atıf Sayısı Verisi Girin", value="0")
        incites_50_dilim = st.text_input("2.1.Incites %50 Dilime Giren Yayın Oranı", value="0")
        incites_10_dilim = st.text_input("2.2.Incites %10 Dilime Giren Yayın Oranı", value="0")
        acik_erisim = st.text_input("2.5. Açık Erişim Yüzdesi",value="0")
        unv_unv_isbirlik = st.text_input("3.1.Üniversite-Üniversite İşbirlikli Yayın Oranı",value="0")
        unv_sanayi = st.text_input("3.2. Üniversite-Sanayi İşbirlikli Yayın Oranı",value="0")
        uluslarararası_isbirlik = st.text_input("3.3. Uluslararası İşbirlikli Yayın Oranı",value="0")
        
        if st.button("Tamamla"):
            data = {
                "1.1. Bilimsel Yayın Sayısı": bilimsel_yayin_sayisi,
                "1.2. Atıf Sayısı": atif_sayisi,
                "2.1.Incites Dergi Etki Değerinde %50’lik Dilime Giren Bilimsel Yayın Oranı  ": incites_50_dilim,
                "2.2.Incites %10 Dilime Giren Yayın Oranı": incites_10_dilim,
                "2.5. Açık Erişim Yüzdesi" : acik_erisim,
                "3.1.Üniversite-Üniversite İşbirlikli Yayın Oranı" : unv_unv_isbirlik,
                "3.2. Üniversite-Sanayi İşbirlikli Yayın Oranı" : unv_sanayi,
                "3.3. Uluslararası İşbirlikli Yayın Oranı" : uluslarararası_isbirlik
            }
            st.session_state.df = pd.DataFrame([data])
            st.session_state.form_tamamlandi = True


    
    elif st.session_state.fakulte_ismi == "BAP":
        ulusal_fon_tutarı = st.text_input("1.4. Ulusal Projelerden Elde Edilen Fon Tutarı Verisi Girin", value="0")
        uluslararası_fon_tutarı = st.text_input("1.5. Uluslararası Proje Fon Tutarı Verisi Girin", value="0")
        patent_basvuru_sayisi = st.text_input("1.6. Patent (Ulusal ve Uluslararası) Başvuru Sayısı Verisi Girin", value="0")

        if st.button("Tamamla"):
            data = {
                "1.4. Ulusal Projelerden Elde Edilen Fon Tutarı Verisi Girin": ulusal_fon_tutarı,
                "1.5. Uluslararası Proje Fon Tutarı Verisi Girin": uluslararası_fon_tutarı,
                "1.6. Patent (Ulusal ve Uluslararası) Başvuru Sayısı Verisi Girin": patent_basvuru_sayisi
            }
            st.session_state.df = pd.DataFrame([data])
            st.session_state.form_tamamlandi = True

    elif st.session_state.fakulte_ismi == "TTO":
        ulusal_patent = st.text_input("1.7. Ulusal Patent Belge Sayısı Verisi Girin", value="0")
        uluslararasi_belge = st.text_input("1.8. Uluslararası Patent Belge Sayısı Verisi Girin", value="0")
        tasarim_belge = st.text_input("1.9. Faydalı Model/Endüstriyel Tasarım Belge Sayısı Verisi Girin", value="0")

        if st.button("Tamamla"):
            data = {
                "1.7. Ulusal Patent Belge Sayısı Verisi Girin": ulusal_patent,
                "1.8. Uluslararası Patent Belge Sayısı Verisi Girin": uluslararasi_belge,
                "1.9. Faydalı Model/Endüstriyel Tasarım Belge Sayısı Verisi Girin": tasarim_belge
            }
            st.session_state.df = pd.DataFrame([data])
            st.session_state.form_tamamlandi = True

    elif st.session_state.fakulte_ismi == "PDO":
        ulusal_patent = st.text_input("1.7. Ulusal Patent Belge Sayısı Verisi Girin", value="0")
        uluslararasi_belge = st.text_input("1.8. Uluslararası Patent Belge Sayısı Verisi Girin", value="0")
        tasarim_belge = st.text_input("1.9. Faydalı Model/Endüstriyel Tasarım Belge Sayısı Verisi Girin", value="0")

        if st.button("Tamamla"):
            data = {
                "1.7. Ulusal Patent Belge Sayısı Verisi Girin": ulusal_patent,
                "1.8. Uluslararası Patent Belge Sayısı Verisi Girin": uluslararasi_belge,
                "1.9. Faydalı Model/Endüstriyel Tasarım Belge Sayısı Verisi Girin": tasarim_belge
            }
            st.session_state.df = pd.DataFrame([data])
            st.session_state.form_tamamlandi = True    

    
    # Form tamamlandıysa "Gönder" butonunu göster
    if st.session_state.form_tamamlandi:
        st.success("Form tamamlandı, şimdi gönderebilirsiniz.")
        
        recipient_email = "umitcaninozu@gmail.com"
        if recipient_email and st.button("Gönder"):
            with io.BytesIO() as buffer:
                with pd.ExcelWriter(buffer) as writer:
                    st.session_state.df.to_excel(writer, index=False, sheet_name='Veriler')
                
                buffer.seek(0)
                excel_data = buffer.getvalue()
            
            subject = "Kriter Verileri"
            body = f"{st.session_state.fakulte_ismi} birimi {st.session_state.unvan} {st.session_state.ad} {st.session_state.soyad} tarafından gönderilen kriter verileri ekte bulunmaktadır."

            
            # E-posta gönderme fonksiyonunu çağırın
            send_email(recipient_email, subject, body, excel_data)
            
            st.session_state.form_gonderildi = True
            st.success("E-posta başarıyla gönderildi.")


                       
                       
