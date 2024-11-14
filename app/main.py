import streamlit as st
import pandas as pd
from app.db.session import get_db
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from app.utils.db_monitor import monitor_db_operation, display_db_monitor

def main():
    st.set_page_config(
        page_title="Axis Program Management",
        page_icon="📊",
        layout="wide"
    )

    # Initialize session state
    if 'current_view' not in st.session_state:
        st.session_state.current_view = 'dashboard'
    if 'selected_project' not in st.session_state:
        st.session_state.selected_project = None

    # Sidebar navigation
    with st.sidebar:
        st.title("Axis Program Management")
        st.markdown("---")
        view = st.radio(
            "Navigation",
            ["Dashboard", "Project Management", "Reports"],
            key="nav"
        )
        st.session_state.current_view = view.lower().replace(" ", "_")
        
        # User info
        st.markdown("---")
        st.markdown(f"User: {get_current_user()}")
        st.markdown(f"Last Login: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    # Main content
    if st.session_state.current_view == 'dashboard':
        render_dashboard()
    elif st.session_state.current_view == 'project_management':
        render_project_management()
    elif st.session_state.current_view == 'reports':
        render_reports()

def get_current_user():
    import getpass
    return getpass.getuser()

def get_project_metrics():
    """Get project metrics from database"""
    try:
        db = next(get_db())
        metrics = {}
        
        # Active Projects
        active_query = """
        SELECT COUNT(*) as count 
        FROM CS_EXP_Project_Translation WITH (NOLOCK)
        WHERE Status IN ('New', 'Active')
        """
        active_df = pd.read_sql(active_query, db.bind)
        metrics['active'] = active_df['count'].iloc[0]
        
        # Pending Reviews
        pending_query = """
        SELECT COUNT(*) as count 
        FROM CS_EXP_Project_Translation WITH (NOLOCK)
        WHERE Status = 'Review'
        """
        pending_df = pd.read_sql(pending_query, db.bind)
        metrics['pending'] = pending_df['count'].iloc[0]
        
        # Completed This Month
        completed_query = """
        SELECT COUNT(*) as count 
        FROM CS_EXP_Project_Translation WITH (NOLOCK)
        WHERE Status = 'Completed' 
        AND LastEditDate >= DATEADD(MONTH, DATEDIFF(MONTH, 0, GETDATE()), 0)
        AND LastEditDate < DATEADD(MONTH, DATEDIFF(MONTH, 0, GETDATE()) + 1, 0)
        """
        completed_df = pd.read_sql(completed_query, db.bind)
        metrics['completed'] = completed_df['count'].iloc[0]
        
        return metrics
    except Exception as e:
        st.error(f"Error fetching metrics: {str(e)}")
        return {'active': 0, 'pending': 0, 'completed': 0}
    finally:
        db.close()

def get_recent_projects():
    """Get recent projects from database"""
    try:
        db = next(get_db())
        query = """
        SELECT TOP 5 
            p.ProjectID,
            p.ProjectType,
            p.ProjectDesc,
            p.Status,
            p.Analyst,
            p.PM,
            CONVERT(VARCHAR(23), p.LastEditDate, 126) as LastEditDate,
            COUNT(n.ProjectID) as NoteCount
        FROM CS_EXP_Project_Translation p WITH (NOLOCK)
        LEFT JOIN CS_EXP_ProjectNotes n WITH (NOLOCK) 
            ON p.ProjectID = n.ProjectID
        GROUP BY 
            p.ProjectID,
            p.ProjectType,
            p.ProjectDesc,
            p.Status,
            p.Analyst,
            p.PM,
            p.LastEditDate
        ORDER BY p.LastEditDate DESC
        """
        df = pd.read_sql(query, db.bind)
        
        # Format the LastEditDate column
        if not df.empty:
            try:
                # More flexible date parsing
                df['LastEditDate'] = pd.to_datetime(
                    df['LastEditDate'],
                    format='mixed',  # Allow mixed formats
                    errors='coerce'  # Replace errors with NaT
                )
                
                # Format only valid dates
                mask = df['LastEditDate'].notna()
                df.loc[mask, 'LastEditDate'] = df.loc[mask, 'LastEditDate'].dt.strftime('%Y-%m-%d %H:%M')
                
                # Fill invalid dates with original value
                df['LastEditDate'] = df['LastEditDate'].fillna('No date available')
                
            except Exception as date_error:
                st.error(f"Error formatting dates: {str(date_error)}")
                # Keep original format if conversion fails
                pass
        
        return df
    except Exception as e:
        st.error(f"Error fetching recent projects: {str(e)}")
        return pd.DataFrame(columns=[
            'ProjectID', 'ProjectType', 'ProjectDesc', 
            'Status', 'Analyst', 'PM', 'LastEditDate', 'NoteCount'
        ])
    finally:
        db.close()

def render_dashboard():
    st.title("Project Dashboard")
    
    # Project Metrics
    metrics = get_project_metrics()
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Active Projects",
            metrics['active'],
            delta=None,
            help="Projects with status New or Active"
        )
    
    with col2:
        st.metric(
            "Pending Reviews",
            metrics['pending'],
            delta=None,
            help="Projects awaiting review"
        )
    
    with col3:
        st.metric(
            "Completed This Month",
            metrics['completed'],
            delta=None,
            help="Projects completed in current month"
        )

    # Recent Projects
    st.markdown("---")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Recent Projects")
        recent_projects = get_recent_projects()
        if recent_projects is not None and not recent_projects.empty:
            st.dataframe(
                recent_projects,
                column_config={
                    "ProjectID": st.column_config.TextColumn(
                        "Project ID",
                        width="medium"
                    ),
                    "ProjectType": st.column_config.TextColumn(
                        "Type",
                        width="small"
                    ),
                    "ProjectDesc": st.column_config.TextColumn(
                        "Description",
                        width="large"
                    ),
                    "Status": st.column_config.TextColumn(
                        "Status",
                        width="medium"
                    ),
                    "Analyst": st.column_config.TextColumn(
                        "Analyst",
                        width="medium"
                    ),
                    "PM": st.column_config.TextColumn(
                        "Project Manager",
                        width="medium"
                    ),
                    "LastEditDate": st.column_config.TextColumn(
                        "Last Updated",
                        width="medium"
                    ),
                    "NoteCount": st.column_config.NumberColumn(
                        "Notes",
                        width="small",
                        format="%d"
                    )
                },
                hide_index=True,
                use_container_width=True
            )
        else:
            st.info("No recent projects found.")
    
    with col2:
        st.subheader("Project Status Distribution")
        status_dist = get_status_distribution()
        if status_dist is not None and not status_dist.empty:
            fig = px.pie(
                status_dist,
                values='count',
                names='Status',
                title='Project Status Distribution',
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No status distribution data available.")

    # Add this at the bottom of the dashboard for debugging
    if st.checkbox("Show Debug Info"):
        debug_date_formats()

def get_status_distribution():
    """Get project status distribution"""
    try:
        db = next(get_db())
        query = """
        SELECT 
            Status, 
            COUNT(*) as count
        FROM CS_EXP_Project_Translation WITH (NOLOCK)
        GROUP BY Status
        ORDER BY 
            CASE Status 
                WHEN 'New' THEN 1
                WHEN 'Active' THEN 2
                WHEN 'Review' THEN 3
                WHEN 'Completed' THEN 4
                ELSE 5
            END
        """
        df = pd.read_sql(query, db.bind)
        return df
    except Exception as e:
        st.error(f"Error fetching status distribution: {str(e)}")
        return None
    finally:
        db.close()

@monitor_db_operation("project_management")
def render_project_management():
    """Render project management view"""
    st.title("Project Management")
    
    # Add database monitor
    if st.checkbox("Show Database Monitor"):
        display_db_monitor()
    
    # Add debug checkbox
    if st.checkbox("Show Database Structure"):
        verify_table_structure()
    
    # Create tabs for project list and new project
    tab1, tab2 = st.tabs(["Project List", "Create New Project"])
    
    with tab1:
        # Filters
        col1, col2 = st.columns([2, 1])
        
        with col1:
            status_filter = st.multiselect(
                "Status Filter",
                ["New", "Active", "Review", "Completed"],
                default=["New", "Active"]
            )
        
        with col2:
            try:
                date_range = st.date_input(
                    "Date Range",
                    value=[
                        datetime.now() - timedelta(days=30),
                        datetime.now()
                    ],
                    max_value=datetime.now()
                )
            except Exception as e:
                st.error(f"Error with date input: {str(e)}")
                date_range = None
        
        # Get filtered projects
        projects_df = get_filtered_projects(
            status_filter=status_filter if status_filter else None,
            date_range=date_range if isinstance(date_range, (list, tuple)) and len(date_range) == 2 else None
        )
        
        if not projects_df.empty:
            # Display projects in a dataframe with selection
            st.dataframe(
                projects_df,
                column_config={
                    "ProjectID": st.column_config.TextColumn(
                        "Project ID",
                        width="medium"
                    ),
                    "ProjectType": st.column_config.TextColumn(
                        "Type",
                        width="small"
                    ),
                    "ProjectDesc": st.column_config.TextColumn(
                        "Description",
                        width="large"
                    ),
                    "Status": st.column_config.TextColumn(
                        "Status",
                        width="medium"
                    ),
                    "LastEditDate": st.column_config.TextColumn(
                        "Last Updated",
                        width="medium"
                    )
                },
                hide_index=True,
                use_container_width=True
            )
            
            # Add a selectbox for project selection
            project_ids = projects_df['ProjectID'].tolist()
            project_descriptions = [
                f"Project {pid}: {desc[:50]}..." 
                for pid, desc in zip(projects_df['ProjectID'], projects_df['ProjectDesc'])
            ]
            
            selected_project_index = st.selectbox(
                "Select a project to view details:",
                range(len(project_ids)),
                format_func=lambda x: project_descriptions[x]
            )
            
            if selected_project_index is not None:
                selected_project_id = project_ids[selected_project_index]
                display_project_details(selected_project_id)
                
        else:
            st.info("No projects found matching the filters.")
    
    with tab2:
        create_new_project()

def get_filtered_projects(status_filter=None, date_range=None):
    """Get filtered projects from database"""
    try:
        db = next(get_db())
        
        # Base query
        query = """
        SELECT 
            ProjectID,
            ProjectType,
            ProjectDesc,
            Status,
            CONVERT(VARCHAR(23), LastEditDate, 126) as LastEditDate
        FROM CS_EXP_Project_Translation WITH (NOLOCK)
        WHERE 1=1
        """
        
        # Initialize parameters as a list
        params = []
        
        # Add status filter if provided
        if status_filter and isinstance(status_filter, list) and len(status_filter) > 0:
            placeholders = ','.join(['?' for _ in status_filter])
            query += f" AND Status IN ({placeholders})"
            # Add each status as a separate parameter
            for status in status_filter:
                params.append(status)
        
        # Add date range filter if provided
        if date_range and isinstance(date_range, (list, tuple)) and len(date_range) == 2:
            query += " AND LastEditDate BETWEEN ? AND ?"
            # Convert dates to string format
            start_date = date_range[0].strftime('%Y-%m-%d 00:00:00')
            end_date = date_range[1].strftime('%Y-%m-%d 23:59:59')
            params.extend([start_date, end_date])
        
        # Add order by
        query += " ORDER BY LastEditDate DESC"
        
        # Execute query with parameters as a tuple
        df = pd.read_sql(query, db.bind, params=tuple(params) if params else None)
        
        # Format dates
        if not df.empty:
            df['LastEditDate'] = pd.to_datetime(
                df['LastEditDate'],
                format='mixed',
                errors='coerce'
            ).dt.strftime('%Y-%m-%d %H:%M')
            
        return df
        
    except Exception as e:
        st.error(f"Error fetching projects: {str(e)}")
        # Log the full error for debugging
        st.error(f"Full error: {type(e).__name__}, {str(e)}")
        return pd.DataFrame(columns=[
            'ProjectID', 'ProjectType', 'ProjectDesc', 
            'Status', 'LastEditDate'
        ])
    finally:
        db.close()

def render_reports():
    st.title("Reports")
    
    report_type = st.selectbox(
        "Select Report Type",
        ["Project Status Summary", "Competitor Analysis", "Service Area Coverage"]
    )
    
    if report_type == "Project Status Summary":
        render_status_report()
    elif report_type == "Competitor Analysis":
        render_competitor_report()
    elif report_type == "Service Area Coverage":
        render_coverage_report()

def render_status_report():
    st.subheader("Project Status Summary")
    
    # Project status over time
    status_data = get_status_over_time()
    if status_data is not None and not status_data.empty:
        fig = px.line(
            status_data,
            x='Month',
            y='Count',
            color='Status',
            title='Project Status Trends'
        )
        st.plotly_chart(fig, use_container_width=True)

def get_status_over_time():
    """Get project status counts over time"""
    try:
        db = next(get_db())
        query = """
        SELECT 
            FORMAT(LastEditDate, 'yyyy-MM') as Month,
            Status,
            COUNT(*) as Count
        FROM CS_EXP_Project_Translation
        WHERE LastEditDate >= DATEADD(month, -12, GETDATE())
        GROUP BY FORMAT(LastEditDate, 'yyyy-MM'), Status
        ORDER BY Month, Status
        """
        df = pd.read_sql(query, db.bind)
        return df
    except Exception as e:
        st.error(f"Error fetching status trends: {str(e)}")
        return None
    finally:
        db.close()

def render_competitor_report():
    st.subheader("Competitor Analysis")
    # Implement competitor analysis visualizations
    st.info("Competitor analysis report coming soon!")

def render_coverage_report():
    st.subheader("Service Area Coverage")
    # Implement service area coverage visualizations
    st.info("Service area coverage report coming soon!")

def debug_date_formats():
    """Debug function to check date formats"""
    try:
        db = next(get_db())
        query = """
        SELECT TOP 5
            ProjectID,
            LastEditDate as OriginalDate,
            CONVERT(VARCHAR(23), LastEditDate, 126) as ISO8601,
            CONVERT(VARCHAR(20), LastEditDate, 120) as Style120,
            CONVERT(VARCHAR(20), LastEditDate, 121) as Style121,
            CONVERT(VARCHAR(20), LastEditDate, 127) as Style127
        FROM CS_EXP_Project_Translation WITH (NOLOCK)
        ORDER BY LastEditDate DESC
        """
        df = pd.read_sql(query, db.bind)
        st.write("Debug: Date Formats")
        st.dataframe(df)
        
        # Show sample date parsing
        if not df.empty:
            st.write("Sample Date Parsing:")
            sample_date = df['ISO8601'].iloc[0]
            st.write(f"Original: {sample_date}")
            try:
                parsed_date = pd.to_datetime(sample_date, format='mixed')
                st.write(f"Parsed: {parsed_date}")
                formatted_date = parsed_date.strftime('%Y-%m-%d %H:%M')
                st.write(f"Formatted: {formatted_date}")
            except Exception as e:
                st.error(f"Parsing error: {str(e)}")
                
    except Exception as e:
        st.error(f"Error in debug: {str(e)}")
    finally:
        db.close()

def create_new_project():
    """Create a new project form"""
    st.subheader("Create New Project")
    
    with st.form("new_project_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            project_type = st.selectbox(
                "Project Type",
                ["Translation", "Review", "QA", "Other"],
                index=None,
                placeholder="Select project type..."
            )
            
            status = st.selectbox(
                "Status",
                ["New", "Active", "Review", "Completed"],
                index=0
            )
            
            analyst = st.text_input(
                "Analyst",
                placeholder="Enter analyst name"
            )
        
        with col2:
            project_desc = st.text_area(
                "Project Description",
                placeholder="Enter project description",
                height=100
            )
            
            pm = st.text_input(
                "Project Manager",
                placeholder="Enter PM name"
            )
        
        submitted = st.form_submit_button("Create Project")
        
        if submitted:
            if not project_type or not project_desc:
                st.error("Project Type and Description are required.")
                return
            
            try:
                db = next(get_db())
                query = """
                INSERT INTO CS_EXP_Project_Translation (
                    ProjectType,
                    ProjectDesc,
                    Status,
                    Analyst,
                    PM,
                    LastEditDate
                ) VALUES (?, ?, ?, ?, ?, GETDATE())
                """
                
                params = [
                    project_type,
                    project_desc,
                    status,
                    analyst,
                    pm
                ]
                
                db.execute(query, params)
                db.commit()
                st.success("Project created successfully!")
                
                # Clear form (by rerunning the app)
                st.experimental_rerun()
                
            except Exception as e:
                st.error(f"Error creating project: {str(e)}")
                db.rollback()
            finally:
                db.close()

@monitor_db_operation("project_details")
def display_project_details(project_id):
    """Display project details with monitoring"""
    try:
        if project_id is None:
            st.warning("Please select a project to view details.")
            return
            
        db = next(get_db())
        query = """
        SELECT 
            p.ProjectID,
            p.ProjectType,
            p.ProjectDesc,
            p.Status,
            p.Analyst,
            p.PM,
            CONVERT(VARCHAR(23), p.LastEditDate, 126) as LastEditDate,
            COUNT(n.ProjectID) as NoteCount
        FROM CS_EXP_Project_Translation p WITH (NOLOCK)
        LEFT JOIN CS_EXP_ProjectNotes n WITH (NOLOCK) 
            ON p.ProjectID = n.ProjectID
        WHERE p.ProjectID = ?
        GROUP BY 
            p.ProjectID,
            p.ProjectType,
            p.ProjectDesc,
            p.Status,
            p.Analyst,
            p.PM,
            p.LastEditDate
        """
        
        # Execute query with properly formatted parameters
        df = pd.read_sql(query, db.bind, params=(str(project_id),))
        
        if not df.empty:
            project = df.iloc[0].to_dict()  # Convert to dictionary for safer access
            
            # Display project details in an expander
            with st.expander("Project Details", expanded=True):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**Project ID:** {project['ProjectID']}")
                    st.markdown(f"**Project Type:** {project['ProjectType']}")
                    st.markdown(f"**Status:** {project['Status']}")
                    st.markdown(f"**Analyst:** {project['Analyst'] or 'Not assigned'}")
                
                with col2:
                    st.markdown(f"**Project Manager:** {project['PM'] or 'Not assigned'}")
                    st.markdown(f"**Notes Count:** {project['NoteCount']}")
                    st.markdown(f"**Last Updated:** {project['LastEditDate']}")
                
                st.markdown("---")
                st.markdown("**Description:**")
                st.write(project['ProjectDesc'] or 'No description available')
            
            # Display notes in a separate expander
            with st.expander("Project Notes", expanded=True):
                display_project_notes(str(project_id))
        else:
            st.warning(f"No details found for Project ID: {project_id}")
            
    except Exception as e:
        st.error(f"Error loading project details: {str(e)}")
        st.error(f"Debug info - Project ID: {project_id}, Type: {type(project_id)}")
    finally:
        db.close()

@monitor_db_operation("project_notes")
def display_project_notes(project_id):
    """Display project notes with monitoring"""
    try:
        db = next(get_db())
        
        # Main query with correct column names
        query = """
        SELECT 
            RecordID,
            ProjectID,
            Notes,
            ProjectStatus,
            LastEditMSID as Author,
            CONVERT(VARCHAR(23), LastEditDate, 126) as NoteDate
        FROM CS_EXP_ProjectNotes WITH (NOLOCK)
        WHERE ProjectID = ?
        ORDER BY LastEditDate DESC
        """
        
        notes_df = pd.read_sql(query, db.bind, params=(str(project_id),))
        
        if not notes_df.empty:
            for _, note in notes_df.iterrows():
                with st.container():
                    st.markdown(f"**{note['Author']} - {note['NoteDate']}**")
                    st.markdown(note['Notes'])
                    if note['ProjectStatus']:
                        st.markdown(f"*Status: {note['ProjectStatus']}*")
                    st.markdown("---")
        else:
            st.info("No notes available for this project.")
            
        # Add new note form
        with st.form(key=f"new_note_{project_id}"):
            new_note = st.text_area("Add a new note")
            status = st.selectbox(
                "Status",
                ["", "New", "Active", "Review", "Completed"],
                index=0
            )
            action_item = st.selectbox(
                "Action Item",
                ["", "Yes", "No"],
                index=0
            )
            
            submit_note = st.form_submit_button("Add Note")
            
            if submit_note and new_note:
                try:
                    insert_query = """
                    INSERT INTO CS_EXP_ProjectNotes (
                        ProjectID,
                        Notes,
                        ProjectStatus,
                        ActionItem,
                        LastEditMSID,
                        LastEditDate,
                        DataLoadDate
                    ) VALUES (?, ?, ?, ?, ?, GETDATE(), GETDATE())
                    """
                    
                    db.execute(
                        insert_query, 
                        (
                            str(project_id),
                            new_note,
                            status if status else None,
                            action_item if action_item else None,
                            st.session_state.get('user', 'Unknown')
                        )
                    )
                    db.commit()
                    st.success("Note added successfully!")
                    st.experimental_rerun()
                except Exception as e:
                    st.error(f"Error adding note: {str(e)}")
                    db.rollback()
                    
    except Exception as e:
        st.error(f"Error loading notes: {str(e)}")
        st.error(f"Debug info - Project ID: {project_id}, Type: {type(project_id)}")
    finally:
        db.close()

def verify_table_structure():
    """Verify database table structure"""
    try:
        db = next(get_db())
        tables = ['CS_EXP_Project_Translation', 'CS_EXP_ProjectNotes']
        
        for table in tables:
            query = f"""
            SELECT 
                COLUMN_NAME,
                DATA_TYPE,
                CHARACTER_MAXIMUM_LENGTH,
                IS_NULLABLE
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME = '{table}'
            ORDER BY ORDINAL_POSITION
            """
            df = pd.read_sql(query, db.bind)
            st.write(f"\nTable: {table}")
            st.dataframe(df)
            
    except Exception as e:
        st.error(f"Error verifying table structure: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    main() 