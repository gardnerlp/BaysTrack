try:
    import streamlit
    print(f"Streamlit is installed. Version: {streamlit.__version__}")
except ImportError:
    print("Streamlit is not installed.")
