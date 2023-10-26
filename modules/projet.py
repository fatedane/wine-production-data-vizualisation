import streamlit as st
from streamlit_folium import st_folium 
import plotly.graph_objects as go
import folium
from folium import plugins

st.title("Application de Visualisation de Données") 



def side_bar ():
    with st.sidebar:
        st.subheader('Tavani')
        st.subheader('Lucas')
        st.subheader('BIA2')
        st.subheader('[Linkedin](www.linkedin.com/in/lucas-tavani-2002z/)')
        st.subheader('[Github](https://github.com/fatedane)')
        st.subheader('Supervised by Djallel DILMI ')

def initialize_map():
    m = folium.Map(
    location=[46.603354, 3],
    zoom_start=6, 
    scrollWheelZoom=False,
    zoom_control=False,
    )
    return m

def display_map (data, géo) :
    m = initialize_map()
    choropleth = create_choropleth(data, géo)
    choropleth.add_to(m)
    colors = create_colors(data, géo)
    colors.add_to(m)
    folium.LayerControl().add_to(m)
    st.markdown("##### Carte de la production de vin en France")
    render_streamlit_map(m, "map")
    legende()

def create_choropleth (data, géo) :
    
    return folium.Choropleth(
        geo_data=géo,
        name='choropleth',
        data=data,
        columns=['code_dep', 'TOTAL'],
        fill_color='YlGn',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Wine Production by Department'
    )
    

def color_producer(data, code):
    department_data = data[data['code_dep'] == code]
    if not department_data.empty:
        total = department_data['TOTAL'].values[0]
        if total == 0:
            return 'white'
        elif 0 < total < 10000:
            return 'pink'
        elif 10000 < total < 1000000:
            return 'red'
        else:
            return 'purple'
    return 'white' 
    
def render_streamlit_map(map, key):
    """Renders the map visualization in the Streamlit app."""
    st_map = st_folium(map, height=350, key=key, use_container_width=True, zoom=5)
    if "dep" not in st.session_state :
        st.session_state["dep"] = "00"
        
    st.write("Cliquez sur un département de la carte pour le séléctionner :")
    if st.button("Cliquez ici pour séléctionner tous les départments"):
        st.session_state["dep"] = "00"
    elif st_map["last_active_drawing"]:
        st.session_state["dep"] = st_map["last_active_drawing"]["properties"]["code"]
        

def create_colors (data, géo):
    return folium.GeoJson(
            géo,
            name='custom colors',
            style_function=lambda feature: {
                'fillColor': color_producer(data, feature['properties']['code']),
                'fillOpacity': 0.7,
                'color': 'black',
                'weight': 1,
            },
        )
        
def legende():
    legend_html = """
    <div style="position: absolute; bottom: 10px; left: 10px; z-index: 1000; background-color: #0E1117; padding: 5px; border-radius: 5px;">
        <p><strong>Légende</strong></p>
        <p><span style="background-color: white; border-radius: 50%; width: 15px; height: 15px; display: inline-block;"></span> Pas de production ou pas de données</p>
        <p><span style="background-color: pink; border-radius: 50%; width: 15px; height: 15px; display: inline-block;"></span> Faible production (0-10k hL)</p>
        <p><span style="background-color: red; border-radius: 50%; width: 15px; height: 15px; display: inline-block;"></span> Production moyenne (10k -1M hL) </p>
        <p><span style="background-color: purple; border-radius: 50%; width: 15px; height: 15px; display: inline-block;"></span> Forte production (> 1M hL) </p>
    </div>
    """
    for _ in range(15):
            st.write('')
    st.markdown(legend_html, unsafe_allow_html=True)
        

    
        
        

        
        
    
def create_productivité_bar(data):
    data = data.iloc[:-1]
    data['productivité'] = data['TOTAL'] / data['superficie totale']
    fig = go.Figure([go.Bar(x=data['num&nom_dep'], y=data['productivité'])])
    fig.update_layout(title_text="productivité au m carré par département")
    return fig

def create_cognac_pie(data):
    data = data.iloc[:-1]
    data = data[data['qte Cognac'].notnull() & (data['qte Cognac'] != 0)]
    fig = go.Figure(data=[go.Pie(labels=data['num&nom_dep'], values=data['qte Cognac'])])
    fig.update_traces(textinfo='percent+label')
    fig.update_layout(title_text="Production de Cognac et d'Armagnac par département")
    return fig

def linear_chart(data):
    data = data.iloc[:-1]
    fig = go.Figure(go.Scatter(x=data['nombre de déclarations'], y=data['TOTAL'], mode='markers', marker=dict(size=8)))
    fig.update_traces(text=data['num&nom_dep'], textposition='top center')
    fig.update_layout(title_text="Productivité par département")
    return fig
    
def top_n_dep_wine(n, wine_type, ordre, data):
    data = data.iloc[:-1]
    data = data[data[wine_type].notnull() & (data[wine_type] != 0)]
    
    if ordre == "plus":
        data= data.sort_values(by=wine_type, ascending=False)
    elif ordre =="moins":
        data = data.sort_values(by=wine_type, ascending=True)
    else :
        st.write('error')

    top_n_departments = data.head(n)

    fig = go.Figure([go.Bar(x=top_n_departments['num&nom_dep'], y=top_n_departments['TOTAL'])])
    tittle = "Les " + str(n) + " départements produisant le " + ordre + " de " + wine_type
    fig.update_layout(title_text=tittle)
    return fig
    
    
def create_pie_chart(data, dep):
    res = data.loc[data['code_dep'] == dep]
    colors = ['#87CEEB', '#FF6B6B', '#FFD700', '#98FB98', '#9370DB']
    labels = ['AOC', 'VDQS', 'autre', 'VDP', 'Cognac']
    values = res["Total AOC"].values[0], res["Total VDQS"].values[0], res["Total autre"].values[0], res["Total VDP"].values[0], res["qte Cognac"].values[0]
    
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, textinfo='label+percent', marker=dict(colors=colors))])
    fig.update_layout(title=f"Répartition de la production de vin en {res['num&nom_dep'].values[0]}")

    return fig

def dispay_choice():
    selected_columns = ["qte totale rouge/rose", "qte AOC blanc", "qte AOC rouge/rose", "qte VDQS blanc", "qte VDQS rouge/rose",
                    "qte VDP blanc", "qte VDP rouge/rose", "qte autre blanc",
                    "qte autre rouge/rose", "qte totale blanc"]
    
    n = st.number_input("Nombre de départements à afficher", min_value=1, value=5)
    wine_type = st.selectbox("Type de vin à afficher", selected_columns)
    ordre = st.radio("Ordre : croissant/décroissant", ["plus", "moins"])
    
    return n, wine_type, ordre

def display_charts (data, dep):
    st.plotly_chart(create_pie_chart(data, dep))
    choice = dispay_choice()
    st.plotly_chart(top_n_dep_wine(choice[0], choice[1], choice[2], data))
    st.plotly_chart(create_productivité_bar(data))
    st.write('La productivité est la production (hL) divisée par la surface de production (m carrés)')
    st.plotly_chart(create_cognac_pie(data))
    st.plotly_chart(linear_chart(data))
    st.write("La productivité est la production (hL) divisée par le nombre de déclarations)")


    
    