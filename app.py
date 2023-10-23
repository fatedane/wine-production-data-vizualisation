import streamlit as st

from modules.projet import (
    side_bar,
    display_map,
    display_charts,
)

from cache import(
    géo_load,
    data_true
)
    
    
def main():
    st.title("Data vizualisation sur la production de vin en France")
    side_bar()
    prod = data_true()
    géo = géo_load()
    display_map(prod, géo)
    display_charts(prod, st.session_state["dep"])
    
    
    
if __name__ == "__main__":
    main()
    