import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt
import plotly.express as px

st.markdown("<h1 style='text-align: center; color: white;'>Kesiapan Infrastruktur Internet Indonesia Menghadapi Perkembangan Ekonomi Digital Pasca COVID-19</h1>", unsafe_allow_html=True)
st.write("Di akhir tahun 2020, tingkat penetrasi internet di Indonesia mencapai 73.7%[[1]](https://apjii.or.id/survei). Pandemi COVID-19 mendorong untuk mengubah cara hidup manusia melalui digitalisasi (sekolah, sistem pembayaran, berdagang, dll..).  Namun, menurut berita dari [Kompas](https://money.kompas.com/read/2022/02/23/153200926/ini-beberapa-hambatan-ekonomi-digital-di-indonesia)[2], Indonesia masih belum memiliki kapabilitas dalam segi intrastruktur yang baik untuk memasuki era digital, apakah benar?")

#SPEEDTEST SEGMENT
st.write('### Kecepatan Internet di Indonesia')
st.write('Kecepatan internet menjadi acuan pertama yang dirasakan pengguna internet dalam mengukur kualitas layanan internet yang digunakan. Bagaimanakah kecepatan internet Indonesia dibandingkan negara ASEAN lainnya?')
#Speedtest Chart------------------------------
speedtest = pd.read_csv('Speedtest Data.csv')
col_rename = speedtest.rename(columns={'Median Mobile Subscriber (Mbps)':'Mobile Subscriber',
                                       'Median Fixed Broadband (Mbps)':'Fixed Broadband'})
plot_speedtest = col_rename.melt(id_vars='Country', value_vars=['Mobile Subscriber', 'Fixed Broadband'],
                                 var_name='Internet_Type', value_name='Median')
plot_speedtest = plot_speedtest.sort_values(['Internet_Type', 'Median'], ascending=[False, False])

fig1 = px.bar(plot_speedtest, x="Country", y="Median",
             color="Internet_Type",
             labels={
                'Median':'Median Speed (Mbps)',
                'Internet_Type':'Internet Type'},
             title='Median Internet Speed in ASEAN 2022',
             barmode = 'group')
fig1.update_layout(
    title={
        'x':0.5,
        'y':0.9
    }
)
st.plotly_chart(fig1)
#----------------------------------------
st.caption('<center>Source: Speedtest by Ooklaa<a href=(https://www.speedtest.net/global-index)>[3]</a></center>', unsafe_allow_html=True)
st.write('')
st.write('89.03% pengguna internet di Indonesia menggunakan Handphone/Tablet[[1]](https://apjii.or.id/survei). Menurut hasil pengukuran dari Ookla (Speedtest) pada Agustus 2022, Indonesia memiliki kecepatan median terlambat ke-2 setelah Kamboja pada kecepatan koneksi Handphone. Kecepatan internet layanan Fixed Broadband (Internet Kabel) di Indonesia pun tidak berada di posisi yang baik.')
st.write('Menurut [KOMINFO](https://aqi.co.id/en/news/duduki-ranking-92-kenapa-internet-di-indonesia-lelet#:~:text=Geographical%20conditions%20in%20Indonesia%20are,failure%20in%20building%20communication%20infrastructure.)[4], hal ini disebabkan kondisi geografis yang sulit dan didominasinya layanan prepaid dengan harga layanan yang murah.')
#Prepaid Chart---------------------------
total_subs = pd.read_csv('mobile_subs.csv')
prepaid = pd.read_csv('prepaid_mobile_subscription.csv')
col_sea = ['Indonesia', 'Myanmar', 'Cambodia', 'Brunei', 'Laos', 'Malaysia', 'Philippines', 'Singapore', 'Thailand',
            'Vietnam']
sea_subs = total_subs[total_subs['Country Name'].isin(col_sea)]
sea_subs = sea_subs[['Country Name', '2020']].reset_index(drop=True)
prepaid_plot = sea_subs.merge(prepaid, left_on='Country Name', right_on='Country', how='left').drop(columns=['Country', 'Type'])
prep_plot = prepaid_plot.rename(columns={'Country Name':'Country', '2020':'Total_Mobile', 'Number':'Prepaid'})
prep_plot['Prepaid_Percentage'] = [i/j*100 for i,j in zip(prep_plot['Prepaid'], prep_plot['Total_Mobile'])]
prep_plot['Unlimited_Percentage'] = [100 - i for i in prep_plot['Prepaid_Percentage']]
prep_plot = prep_plot.sort_values('Prepaid_Percentage', ascending=False).reset_index(drop=True)

fig2 = px.bar(
    prep_plot,
    x="Country",
    y=["Prepaid_Percentage", "Unlimited_Percentage"],
    labels={
        'value':'Subscriber Rate (%)',
        'variable':'Service'},
    title="Prepaid Subscriber & Unlimited Subscriber in ASEAN 2020"
    )
fig2.update_layout(
    title={
        'x':0.25,
        'y':0.9
    }
)
st.plotly_chart(fig2)
#---------------------------------------------
st.caption(
    '''<center>Source: Mobile Subsciber Data Worldbank<a href=https://data.worldbank.org/indicator/IT.CEL.SETS?locations=ID>
    [5]</a> & Prepaid Subscriber Datahub ITU<a href=https://datahub.itu.int/data/?i=193>[6]</a></center>''',
    unsafe_allow_html=True)
st.write('')
st.write('Pada tahun 2020, 98% pengguna Mobile Subscriber di Indonesia menggunakan layanan Prepaid, yang merupakan ke-2 terbesar pada negara ASEAN berdasarkan rasionya.')

#CAPACITY SEGMENT
st.write('### Kapasitas Internet di Indonesia')
st.write('Populasi di Indonesia tentunya merupakan faktor utama dalam banyaknya data yang digunakan. Penggunaan data dalam jumlah yang sangat besar perlu diiringi dengan kapasitas Internet yang memadai, berikut gambaran rasio banyaknya jumlah data dan kapasitas di setiap negara ASEAN:')
#Capacity vs Usage Bar Chart---------------------
usage = pd.read_csv('international-bandwidth-usage.csv')
capacity = pd.read_csv('lit-equipped-international-bandwidth-capacity.csv')

us_sea = usage[usage['countryName'].isin(col_sea)]
cap_sea = capacity[capacity['countryName'].isin(col_sea)]

us_sea_2020 = us_sea[us_sea['dataYear']==2020]
cap_sea_2020 = cap_sea[cap_sea['dataYear']==2020]

us_sea_2020 = us_sea_2020[['countryName', 'answer1']].reset_index(drop=True).rename(columns={'answer1':'Bandwidth_Usage'})
cap_sea_2020 = cap_sea_2020[['countryName', 'answer1']].reset_index(drop=True).rename(columns={'answer1':'Bandwidth_Capacity'})

bwplot = us_sea_2020.merge(cap_sea_2020, on='countryName', how='left')

bwplot['perc_usage'] = [i / j * 100 for i,j in zip(bwplot['Bandwidth_Usage'], bwplot['Bandwidth_Capacity'])]
bwplot['perc_capacity'] = [100 - i for i in bwplot['perc_usage']]

bwplot = bwplot.sort_values('perc_capacity', ascending=False).reset_index(drop=True)

fig3 = px.bar(
    bwplot,
    x="countryName",
    y=["perc_capacity", "perc_usage"],
    labels={
        'value':'Ratio of Internet Capacity-Usage (%)',
        'countryName':'Country',
        'variable':'Ratio Indicator'
    },
    title="Rate of Internet Usage & Capacity in ASEAN 2020"
    )

fig3.update_layout(
    title={
        'x':0.5,
        'y':0.9
    }
)
st.plotly_chart(fig3)
#---------------------------------------------------------
st.caption(
    '''<center>Source: Bandwidth Capacity Datahub ITU<a href=https://datahub.itu.int/data/?i=19255>[7]</a>
    & Bandwidth Usage Datahub ITU<a href=https://datahub.itu.int/data/?i=242>[8]</a></center>''',
    unsafe_allow_html=True)
st.write('')
st.write('Kapasitas internet di Indonesia masih mampu memfasilitasi banyaknya jumlah data yang dibutuhkan, walau butuh diperhatikan karena sudah menembus 50% dari total kapasitas.')
#Pie Chart Capacity-Usage---------------------------------
st.write('Grafik di atas menunjukkan kapasitas dan penggunaan internet di setiap negaranya. Bagaimana dengan rasio perbandingan kapasitas dan penggunaan internet se-ASEAN?')
import plotly.graph_objects as go
from plotly.subplots import make_subplots

bwplot = bwplot.sort_values('Bandwidth_Capacity', ascending=False).reset_index(drop=True)
top_4 = bwplot[:4]
new_row = pd.DataFrame(data={
    'countryName':['Others'],
    'Bandwidth_Capacity':[bwplot['Bandwidth_Capacity'][4:].sum()],
    'Bandwidth_Usage':[bwplot['Bandwidth_Usage'][4:].sum()]
})
piebw = pd.concat([top_4, new_row])
fig4 = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]])
fig4.add_trace(go.Pie(labels=piebw['countryName'], values=piebw['Bandwidth_Capacity'], name="Bandwidth Capacity"),
              1, 1)
fig4.add_trace(go.Pie(labels=piebw['countryName'], values=piebw['Bandwidth_Usage'], name="Bandwidth Usage"),
              1, 2)
fig4.update_traces(hole=.4, hoverinfo="label+percent+name", textposition='inside', textfont_size=14)
fig4.update_layout(
    title_text="Ratio of Internet Capacity & Usage in ASEAN 2020",
    title={
        'x':0.5,
        'y':0.9
    },
    # Add annotations in the center of the donut pies.
    annotations=[dict(text='Capacity', x=0.15, y=0.5, font_size=20, showarrow=False),
                 dict(text='Usage', x=0.83, y=0.5, font_size=20, showarrow=False)])
st.plotly_chart(fig4)
#-------------------------------------------------
st.caption(
    '''<center>Source: Bandwidth Capacity Datahub ITU<a href=https://datahub.itu.int/data/?i=19255>[7]</a>
    & Bandwidth Usage Datahub ITU<a href=https://datahub.itu.int/data/?i=242>[8]</a></center>''',
    unsafe_allow_html=True)
st.write('')
st.write('Ternyata walaupun penggunaan data Indonesia dua kali lipat lebih banyak dari Malaysia (28% - 12.6%), Indonesia masih memiliki jumlah kapasitas Bandwidth yang lebih sedikit (13.8% - 16.4%).')

#SECURE SERVER
st.write('### Tingkat Keamanan Internet di Indonesia')
st.write('Dalam menulusuri website-website di Internet, belum tentu halaman yang kita klik sudah terlindungi dari pihak-pihak luar yang mencoba mengambil data-data pribadi (hacking, phishing, snooping). Setiap website yang sudah dilandasi Secure Server memastikan transaksi online-nya terlindungi.')
#Time Series Secure Server---------------------------
mobile_inet = pd.read_csv('mobile_subs.csv')
secure_server = pd.read_csv('secure_server.csv')
fixed_broadband = pd.read_csv('fixed_broadband.csv')

column_del = ['1960', '1961', '1962', '1963', '1964', '1965', '1966', '1967', '1968',
       '1969', '1970', '1971', '1972', '1973', '1974', '1975', '1976', '1977',
       '1978', '1979', '1980', '1981', '1982', '1983', '1984', '1985', '1986',
       '1987', '1988', '1989', '1990', '1991', '1992', '1993', '1994', '1995',
       '1996', '1997', '1998', '1999', '2000', '2001', '2002', '2003', '2004',
       '2005', '2006', '2007', '2008', '2009', '2021']

mobile_inet = mobile_inet.drop(columns=column_del)
secure_server = secure_server.drop(columns=column_del)
fixed_broadband = fixed_broadband.drop(columns=column_del)

col_drop_ina = ['Country Code', 'Indicator Name', 'Indicator Code']

mobile_inet = mobile_inet.drop(columns=col_drop_ina)
secure_server = secure_server.drop(columns=col_drop_ina)
fixed_broadband = fixed_broadband.drop(columns=col_drop_ina)

#stream widget section
col_select = ['Indonesia', 'Myanmar', 'Malaysia', 'Philippines', 'Singapore', 'Thailand', 'Vietnam']
tickselect = st.selectbox('Pick Country', col_select)

mobile_inet_sea = mobile_inet[mobile_inet['Country Name']==tickselect]
secure_server_sea = secure_server[secure_server['Country Name']==tickselect]
fixed_broadband_sea = fixed_broadband[secure_server['Country Name']==tickselect]

mobile_inet_sea = mobile_inet_sea.set_index(['Country Name']).transpose().reset_index().rename_axis(columns=None)
secure_server_sea = secure_server_sea.set_index(['Country Name']).transpose().reset_index().rename_axis(columns=None)
fixed_broadband_sea = fixed_broadband_sea.set_index(['Country Name']).transpose().reset_index().rename_axis(columns=None)

mobile_inet_sea = mobile_inet_sea.rename(columns={'index':'Year', tickselect:'Mobile Subscriber'})
secure_server_sea = secure_server_sea.rename(columns={'index':'Year', tickselect:'Secure Server'})
fixed_broadband_sea = fixed_broadband_sea.rename(columns={'index':'Year', tickselect:'Fixed Broadband'})

mbl_vs_srvr = mobile_inet_sea.merge(secure_server_sea, how='left', left_on='Year', right_on='Year').merge(fixed_broadband_sea,
                                                                                                          how='left', on='Year')
#Percentage section
y_mobile=[]
for x in range(len(mbl_vs_srvr['Mobile Subscriber'])):
  if mbl_vs_srvr.loc[x, 'Year'] == '2010':
    y_mobile.append(0)
  else:
    q_mobile = mbl_vs_srvr.loc[0, 'Mobile Subscriber']
    w_mobile = mbl_vs_srvr.loc[x, 'Mobile Subscriber']-q_mobile
    z_mobile = w_mobile/q_mobile*100
    y_mobile.append(z_mobile)
mbl_vs_srvr['Mobile Subscriber perc'] = y_mobile

y_server=[]
for x in range(len(mbl_vs_srvr['Secure Server'])):
  if mbl_vs_srvr.loc[x, 'Year'] == '2010':
    y_server.append(0)
  else:
    q_server = mbl_vs_srvr.loc[0, 'Secure Server']
    w_server = mbl_vs_srvr.loc[x, 'Secure Server']-q_server
    z_server = w_server/q_server*100
    y_server.append(z_server)
mbl_vs_srvr['Secure Server perc'] = y_server

#plot section
fig5 = make_subplots(specs=[[{"secondary_y": True}]])
fig5.add_trace(
    go.Scatter(x=mbl_vs_srvr['Year'], y=mbl_vs_srvr['Mobile Subscriber perc'], name="Mobile Subscriber"),
    secondary_y=False,
)
fig5.add_trace(
    go.Scatter(x=mbl_vs_srvr['Year'], y=mbl_vs_srvr['Secure Server perc'], name="Secure Server"),
    secondary_y=True,
)
fig5.update_layout(
    title_text="Mobile Subscriber & Secure Server Growth Rate in ASEAN",
    title={
        'x':0.45,
        'y':0.9
    }
)
fig5.update_xaxes(
    title_text='Year',
    showgrid=True)
fig5.update_yaxes(showgrid=False)
fig5.update_yaxes(title_text="Mobile Susbcriber Growth Rate (%)", secondary_y=False)
fig5.update_yaxes(title_text="Secure Server Growth Rate (%)", secondary_y=True)
st.plotly_chart(fig5)
#-------------------------------------------------------
st.caption(
    '''<center>Source: Mobile Subsciber Data Worldbank<a href=https://data.worldbank.org/indicator/IT.CEL.SETS?locations=ID>[5]</a>
    & Secure Server Data Worldbank<a href=https://data.worldbank.org/indicator/IT.NET.SECR?locations=ID>[9]</a></center>''',
    unsafe_allow_html=True)
st.write('')
st.write('Karena [kebijakan KOMINFO di akhir tahun 2017](https://nuscri.org/media/static/images/thumbnail-pdf/WCBAUG28SEP032018_PTIGjpr.pdf)[10], jumlah Mobile Subscriber turun drastis. Ini wujud dari KOMINFO untuk mengurangi jumlah nomor bayangan dalam melakukan modus penipuan. Terlebih lagi laju peningkatan Secure Server di Indonesia jauh melampaui jumlah pertumbuhan Mobile Subscriber yang merupakan indikator baik.')

server_1mil = pd.read_csv('secure_internet_server_per1mil.csv')

#widget section
multiselect = st.multiselect(
    'Select Countries:',
    col_select
)
server_1mil = server_1mil[server_1mil['Country Name'].isin(multiselect)]

#drop column
server_1mil = server_1mil.drop(columns=column_del)
server_1mil = server_1mil.drop(columns=['Country Code', 'Indicator Name', 'Indicator Code'])

#transpose dan rename
server_sea_plot = server_1mil.set_index(['Country Name']).transpose().reset_index()
server_sea_plot = server_sea_plot.rename(columns={'index':'Year'}).rename_axis(index=None, columns=None)

#plot section
fig6 = px.line(
    server_sea_plot,
    x='Year',
    y=multiselect,
    labels={
        'variable':'Country'
    }
    )
fig6.update_layout(
    title_text="Secure Server Growth per 1 Million People Rate in ASEAN",
    title={
        'x':0.47,
        'y':0.95
    }
)
fig6.update_yaxes(title_text="Secure Server per 1 Million People")
fig6.update_xaxes(title_text='Year', showgrid=False)
st.plotly_chart(fig6)
#---------------------------------------------------------
st.caption(
    '''<center>Source: Secure Internet Server (per 1 million people) Data Worldbank
    <a href=https://data.worldbank.org/indicator/IT.NET.SECR.P6?locations=ID>[11]</a></center>''',
    unsafe_allow_html=True)
st.write('')
st.write('Dalam segi infrastruktur kemanan, Singapura jauh di atas negara ASEAN lainnya. Walaupun jumlah perkembangan Secure Server  di Indonesia akhir-akhir ini melesat, begitupun juga di beberapa negara ASEAN lainnya. Ternyata dalam segi infrastruktur keamanan pun Indonesia masih butuh ditingkatkan.')

#PENUTUP
st.write('### Jadi, Bagaimanakah Kesiapan Infrastruktur di Indonesia?')
st.write('Dari berbagai data di atas, kita bisa menarik kesimpulan:')
st.markdown('* Kurangnya minat masyarakat terhadap layanan unlimited mempengaruhi market sehingga didominasinya layanan prepaid dengan harga yang murah dan dengan kecepatan yang standar')
st.markdown('* Kapasitas bandwidth di Indonesia masih mencukupi, melihat kapasitas masih tersisa ~40% dari penggunaan')
st.markdown('* Pola pertambahan Secure Server di Indonesia jauh melebihi pola pertambahan Mobile Subscriber, terlebih lagi keseriusan KOMINFO dalam meningkatkan keamanan dengan mengurangi nomor-nomor yang tidak teverifikasi di akhir tahun 2017.')

#SARAN
st.write('### Apa yang Bisa Ditingkatkan Untuk Indonesia Dalam Mempersiapkan Ekonomi Digital?')
st.write(
    '''Dalam meningkatkan kualitas internet pada kategori Mobile, Indonesia memerlukan investasi ke teknologi
    baru bernama 5G. Hal ini bisa dilihat bahwa pada [coverage layanan 5G di Indonesia](https://www.nperf.com/en/map/5g)[12]
    masih sangat minim. Penulis juga mengharapkan provider jaringan Fixed Broadband (fiber optik) di Indonesia
    benar-benar mengimplementasikan paket Unlimited seseungguhnya, dimana provider tidak mengurangi kecepatan internet pelanggan
    ketika sudah mencapai penggunaan Bandwidth tertentu.'''
)
st.write(
    '''Kapasitas bandwidth di Indonesia masih butuh ditingkatkan
    walaupun masih mencukupi, hal ini dikarenakan kapasitas Bandwidth di Indonesia dibawah Malaysia
    padahal penggunaan Bandwidth di Indonesia terbesar ke-2 se-ASEAN (dibawah Singapura). Ini juga butuh diperhatikan
    sebagai bentuk antisipasi perkembangan teknologi dan tingkat penetrasi pengguna internet di Indonesia
    untuk kedepannya.
    ''')
st.write(
    '''Perkembangan keamanan internet di Indonesia pada aspek penyediaan Secure Server sudah sangat baik. Namun
    sama halnya dengan kapasitas Bandwidth, penggunaan Bandwidth yang besar di Indonesia menandakan banyaknya
    transaksi online yang terjadi dibandingkan dengan negara lain. Tren positif dari penyediaan Secure Server
    harus dijaga agar warga Indonesia merasa aman dalam melakukan kegiatan ekonomi digital sehingga mendorong
    minat transaksi digital.'''
)
st.markdown('##### <u>Catatan</u>', unsafe_allow_html=True)
st.markdown(
    '''- Penulis menyadari bahwa kondisi geografi Indonesia yang unik menjadi salah satu penyebab yang penting
    terhambatnya infrastruktur internet di Indonesia, namun dikarenakan tidak ditemukannya pengkategorian
    negara berdasarkan kondisi geografis dari sumber yang kredibel maka penulis memilih untuk tidak menyertainya'''
    )
st.markdown(
    '''- Majoritas data terbaru yang terpapar adalah data pada tahun 2020, hal ini dikarenakan data-data yang
    ditampilkan membutuhkan pengukuran yang teliti dari lembaga-lembaga yang bertanggungjawab di negaranya
    masing-masing''')
st.write('')
st.write('')
st.write('')
st.caption('Contact Me: salmanzf@ymail.com')
