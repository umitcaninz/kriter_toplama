import streamlit as st
import pandas as pd
import io
from sklearn.preprocessing import MinMaxScaler
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication




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
    st.title("Kriter Giriş Ekranı")
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


                       
                       
