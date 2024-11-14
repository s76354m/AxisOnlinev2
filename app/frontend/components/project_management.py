import streamlit as st
import pandas as pd
from datetime import datetime
import requests
from typing import Dict, Optional

class ProjectManagement:
    def __init__(self):
        self.api_url = "http://localhost:8000/api/v1"
        self.project_types = ['A', 'B', 'C']
        self.statuses = ['New', 'Active', 'On Hold', 'Completed', 'Cancelled']

    def render_project_details(self, project_id: str = None):
        if project_id:
            st.title(f"Project Details: {project_id}")
        else:
            st.title("New Project")

        tabs = st.tabs([
            "Project Info",
            "Competitors",
            "Service Areas",
            "Y-Line",
            "Notes"
        ])

        with tabs[0]:
            self.render_project_info(project_id)
        
        with tabs[1]:
            self.render_competitors(project_id)
        
        with tabs[2]:
            self.render_service_areas(project_id)
        
        with tabs[3]:
            self.render_yline(project_id)
        
        with tabs[4]:
            self.render_notes(project_id)

    def render_project_info(self, project_id: str = None):
        with st.form("project_info_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                project_id_input = st.text_input(
                    "Project ID*",
                    value=project_id if project_id else "",
                    disabled=bool(project_id),
                    max_chars=12
                )
                
                project_type = st.selectbox(
                    "Project Type*",
                    options=self.project_types
                )
                
                analyst = st.text_input("Analyst")
                go_live_date = st.date_input("Go Live Date")
            
            with col2:
                benchmark_file = st.text_input("Benchmark File ID")
                description = st.text_area("Description", max_chars=100)
                pm = st.text_input("Project Manager")
                max_mileage = st.number_input("Max Mileage", min_value=0.0)
            
            new_market = st.checkbox("New Market")
            
            if st.form_submit_button("Save Project Info"):
                self.save_project_info({
                    'ProjectID': project_id_input,
                    'ProjectType': project_type,
                    'ProjectDesc': description,
                    'Analyst': analyst,
                    'PM': pm,
                    'GoLiveDate': go_live_date.isoformat(),
                    'MaxMileage': max_mileage,
                    'NewMarket': new_market,
                    'BenchmarkFileID': benchmark_file
                })

    def render_competitors(self, project_id: str):
        st.subheader("Competitors")
        
        # Add competitor form
        with st.form("competitor_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                strenuus_code = st.text_input("Strenuus Product Code", max_chars=50)
                payor = st.text_input("Payor", max_chars=50)
                product = st.text_input("Product", max_chars=60)
            
            with col2:
                ei = st.checkbox("EI")
                cs = st.checkbox("CS")
                mr = st.checkbox("MR")
            
            if st.form_submit_button("Add Competitor"):
                self.save_competitor({
                    'ProjectID': project_id,
                    'StrenuusProductCode': strenuus_code,
                    'Payor': payor,
                    'Product': product,
                    'EI': ei,
                    'CS': cs,
                    'MR': mr
                })
        
        # Display existing competitors with edit/delete options
        competitors = self.get_competitors(project_id)
        if competitors is not None and not competitors.empty:
            for idx, competitor in competitors.iterrows():
                with st.expander(f"Competitor: {competitor['Payor']} - {competitor['Product']}"):
                    with st.form(f"edit_competitor_{competitor['RecordID']}"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            strenuus_code = st.text_input(
                                "Strenuus Product Code",
                                value=competitor['StrenuusProductCode'],
                                key=f"strenuus_{competitor['RecordID']}"
                            )
                            payor = st.text_input(
                                "Payor",
                                value=competitor['Payor'],
                                key=f"payor_{competitor['RecordID']}"
                            )
                            product = st.text_input(
                                "Product",
                                value=competitor['Product'],
                                key=f"product_{competitor['RecordID']}"
                            )
                        
                        with col2:
                            ei = st.checkbox("EI", value=competitor['EI'], key=f"ei_{competitor['RecordID']}")
                            cs = st.checkbox("CS", value=competitor['CS'], key=f"cs_{competitor['RecordID']}")
                            mr = st.checkbox("MR", value=competitor['MR'], key=f"mr_{competitor['RecordID']}")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.form_submit_button("Update"):
                                self.update_competitor(competitor['RecordID'], {
                                    'StrenuusProductCode': strenuus_code,
                                    'Payor': payor,
                                    'Product': product,
                                    'EI': ei,
                                    'CS': cs,
                                    'MR': mr
                                })
                        with col2:
                            if st.form_submit_button("Delete", type="primary"):
                                if st.warning("Are you sure you want to delete this competitor?"):
                                    self.delete_competitor(competitor['RecordID'])
                                    st.rerun()

    def update_competitor(self, record_id: int, data: Dict):
        try:
            response = requests.put(
                f"{self.api_url}/competitors/{record_id}",
                json=data
            )
            if response.status_code == 200:
                st.success("Competitor updated successfully!")
            else:
                st.error(f"Error updating competitor: {response.json().get('detail', 'Unknown error')}")
        except Exception as e:
            st.error(f"Error: {str(e)}")

    def delete_competitor(self, record_id: int):
        try:
            response = requests.delete(f"{self.api_url}/competitors/{record_id}")
            if response.status_code == 200:
                st.success("Competitor deleted successfully!")
            else:
                st.error(f"Error deleting competitor: {response.json().get('detail', 'Unknown error')}")
        except Exception as e:
            st.error(f"Error: {str(e)}")

    def render_service_areas(self, project_id: str):
        st.subheader("Service Areas")
        
        # Add service area form
        with st.form("service_area_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                region = st.text_input("Region", max_chars=30)
                state = st.text_input("State", max_chars=2)
                county = st.text_input("County", max_chars=75)
            
            with col2:
                report_include = st.selectbox("Report Include", ['Y', 'N'])
                max_mileage = st.number_input("Max Mileage", min_value=0)
            
            if st.form_submit_button("Add Service Area"):
                self.save_service_area({
                    'ProjectID': project_id,
                    'Region': region,
                    'State': state,
                    'County': county,
                    'ReportInclude': report_include,
                    'MaxMileage': max_mileage
                })
        
        # Display existing service areas with edit/delete options
        service_areas = self.get_service_areas(project_id)
        if service_areas is not None and not service_areas.empty:
            for idx, area in service_areas.iterrows():
                with st.expander(f"Service Area: {area['Region']} - {area['County']}"):
                    with st.form(f"edit_service_area_{area['RecordID']}"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            region = st.text_input("Region", value=area['Region'], key=f"region_{area['RecordID']}")
                            state = st.text_input("State", value=area['State'], key=f"state_{area['RecordID']}")
                            county = st.text_input("County", value=area['County'], key=f"county_{area['RecordID']}")
                        
                        with col2:
                            report_include = st.selectbox(
                                "Report Include",
                                ['Y', 'N'],
                                index=0 if area['ReportInclude'] == 'Y' else 1,
                                key=f"include_{area['RecordID']}"
                            )
                            max_mileage = st.number_input(
                                "Max Mileage",
                                value=area['MaxMileage'],
                                key=f"mileage_{area['RecordID']}"
                            )
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.form_submit_button("Update"):
                                self.update_service_area(area['RecordID'], {
                                    'Region': region,
                                    'State': state,
                                    'County': county,
                                    'ReportInclude': report_include,
                                    'MaxMileage': max_mileage
                                })
                        with col2:
                            if st.form_submit_button("Delete", type="primary"):
                                if st.warning("Are you sure you want to delete this service area?"):
                                    self.delete_service_area(area['RecordID'])
                                    st.rerun()

    def render_yline(self, project_id: str):
        st.subheader("Y-Line Translation")
        
        with st.form("yline_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                prod_cd = st.text_input("NDB Yline Product Code", max_chars=2)
                ipa = st.number_input("NDB Yline IPA", min_value=0)
            
            with col2:
                mkt_num = st.number_input("NDB Yline Market Number", min_value=0)
                pre_award = st.number_input("Pre Award", min_value=0)
            
            if st.form_submit_button("Add Y-Line"):
                self.save_yline({
                    'ProjectID': project_id,
                    'NDB_Yline_ProdCd': prod_cd,
                    'NDB_Yline_IPA': ipa,
                    'NDB_Yline_MktNum': mkt_num,
                    'PreAward': pre_award
                })
        
        # Display existing Y-Lines
        ylines = self.get_ylines(project_id)
        if ylines is not None:
            st.dataframe(ylines)

    def render_notes(self, project_id: str):
        st.subheader("Project Notes")
        
        with st.form("notes_form"):
            notes = st.text_area("Notes")
            col1, col2 = st.columns(2)
            
            with col1:
                action_item = st.selectbox("Action Item", ['Yes', 'No'])
                project_category = st.text_input("Project Category", max_chars=50)
            
            if st.form_submit_button("Add Note"):
                self.save_note({
                    'ProjectID': project_id,
                    'Notes': notes,
                    'ActionItem': 'Y' if action_item == 'Yes' else 'N',
                    'ProjectCategory': project_category
                })
        
        # Display existing notes
        notes = self.get_notes(project_id)
        if notes is not None:
            st.dataframe(notes)

    # API interaction methods
    def save_project_info(self, data: Dict):
        endpoint = f"{self.api_url}/projects/"
        method = "POST" if not data.get('RecordID') else "PUT"
        self._make_api_request(endpoint, method, data)

    def save_competitor(self, data: Dict):
        self._make_api_request(f"{self.api_url}/competitors/", "POST", data)

    def save_service_area(self, data: Dict):
        self._make_api_request(f"{self.api_url}/service-areas/", "POST", data)

    def save_yline(self, data: Dict):
        self._make_api_request(f"{self.api_url}/ylines/", "POST", data)

    def save_note(self, data: Dict):
        self._make_api_request(f"{self.api_url}/notes/", "POST", data)

    def _make_api_request(self, endpoint: str, method: str, data: Dict):
        try:
            if method == "POST":
                response = requests.post(endpoint, json=data)
            else:
                response = requests.put(endpoint, json=data)
            
            if response.status_code == 200:
                st.success("Data saved successfully!")
            else:
                st.error(f"Error saving data: {response.json().get('detail', 'Unknown error')}")
        except Exception as e:
            st.error(f"Error: {str(e)}")

    # Data retrieval methods
    def get_competitors(self, project_id: str) -> Optional[pd.DataFrame]:
        return self._get_data(f"{self.api_url}/competitors/{project_id}")

    def get_service_areas(self, project_id: str) -> Optional[pd.DataFrame]:
        return self._get_data(f"{self.api_url}/service-areas/{project_id}")

    def get_ylines(self, project_id: str) -> Optional[pd.DataFrame]:
        return self._get_data(f"{self.api_url}/ylines/{project_id}")

    def get_notes(self, project_id: str) -> Optional[pd.DataFrame]:
        return self._get_data(f"{self.api_url}/notes/{project_id}")

    def _get_data(self, endpoint: str) -> Optional[pd.DataFrame]:
        try:
            response = requests.get(endpoint)
            if response.status_code == 200:
                data = response.json()
                return pd.DataFrame(data)
            return None
        except Exception as e:
            st.error(f"Error fetching data: {str(e)}")
            return None 