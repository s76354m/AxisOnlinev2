from sqlalchemy import inspect, MetaData, text
from app.db.session import engine
from app.models import (Project, CSPLOB, YLine, Competitor, 
                       ServiceArea, ProjectNotes)
import streamlit as st

def verify_model_schema(model_class):
    """Verify individual model schema against database"""
    inspector = inspect(engine)
    table_name = model_class.__tablename__
    
    # Get database columns
    db_columns = {
        c['name']: c for c in inspector.get_columns(table_name)
    }
    
    # Get model columns
    model_columns = {
        c.name: c for c in model_class.__table__.columns
    }
    
    return {
        'table_name': table_name,
        'missing_columns': set(model_columns.keys()) - set(db_columns.keys()),
        'extra_columns': set(db_columns.keys()) - set(model_columns.keys()),
        'column_types': [
            (name, str(col.type), str(db_columns[name]['type']))
            for name, col in model_columns.items()
            if name in db_columns
        ]
    }

def verify_all_models():
    """Verify all models against database schema"""
    models = [Project, CSPLOB, YLine, Competitor, ServiceArea, ProjectNotes]
    results = []
    
    for model in models:
        try:
            result = verify_model_schema(model)
            results.append(result)
        except Exception as e:
            results.append({
                'table_name': model.__tablename__,
                'error': str(e)
            })
    
    return results

def display_model_verification():
    """Display model verification results in Streamlit"""
    st.subheader("Database Model Verification")
    
    results = verify_all_models()
    for result in results:
        with st.expander(f"Table: {result['table_name']}", expanded=False):
            if 'error' in result:
                st.error(f"Verification Error: {result['error']}")
                continue
                
            if result['missing_columns']:
                st.warning(f"Missing columns: {', '.join(result['missing_columns'])}")
            if result['extra_columns']:
                st.info(f"Extra columns in DB: {', '.join(result['extra_columns'])}")
            
            st.write("Column Type Comparison:")
            df = pd.DataFrame(result['column_types'], 
                            columns=['Column', 'Model Type', 'DB Type'])
            st.dataframe(df) 