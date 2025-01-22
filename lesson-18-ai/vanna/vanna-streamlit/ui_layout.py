# this dict config UI layout for form-view
COLUMN_PROPS = {

't_config': {
    # Col_1
    'llm_vendor': {
        'is_system_col': False,
        'is_user_key': False,
        'is_required': False,
        'is_visible': True,
        'is_editable': True,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_1-1',
        'widget_type': 'text_input',
        'label_text': 'LLM Vendor'
    },
    'llm_model': {
        'is_system_col': False,
        'is_user_key': False,
        'is_required': True,
        'is_visible': True,
        'is_editable': True,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_1-2',
        'widget_type': 'text_input',
        'label_text': 'LLM Model'
    },
    'db_type': {
        'is_system_col': False,
        'is_user_key': False,
        'is_required': True,
        'is_visible': True,
        'is_editable': True,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_1-3',
        'widget_type': 'text_input',
        'label_text': 'Database'
    },
    'vector_db': {
        'is_system_col': False,
        'is_user_key': False,
        'is_required': True,
        'is_visible': True,
        'is_editable': True,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_1-4',
        'widget_type': 'text_input',
        'label_text': 'VectorStore'
    },
    'note': {
        'is_system_col': False,
        'is_user_key': False,
        'is_required': False,
        'is_visible': True,
        'is_editable': True,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_1-5',
        'widget_type': 'text_area',
        'label_text': 'Note'
    },

    # Col_2
    'id': {
        'is_system_col': True,
        'is_user_key': False,
        'is_required': True,
        'is_visible': True,
        'is_editable': False,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_2-1',
        'widget_type': 'text_input',
        'label_text': 'ID'
    },

    'db_url': {
        'is_system_col': False,
        'is_user_key': False,
        'is_required': True,
        'is_visible': True,
        'is_editable': True,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_2-3',
        'widget_type': 'text_input',
        'label_text': 'Database URL'
    },

    'updated_at': {
        'is_system_col': False,
        'is_user_key': False,
        'is_required': False,
        'is_visible': False,
        'is_editable': False,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_2-4',
        'widget_type': 'text_input',
        'label_text': 'Created At'
    },
    'is_active': {
        'is_system_col': False,
        'is_user_key': False,
        'is_required': False,
        'is_visible': False,
        'is_editable': True,
        'is_clickable': False,
        'datatype': 'integer',
        'form_column': 'COL_2-5',
        'widget_type': 'selectbox',
        'label_text': 'Active?'
    },
}, 

't_note': {
    # Col_1
    'note_name': {
        'is_system_col': False,
        'is_user_key': True,
        'is_required': True,
        'is_visible': True,
        'is_editable': True,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_1-1',
        'widget_type': 'text_input',
        'label_text': 'Title'
    },
    'url': {
        'is_system_col': False,
        'is_user_key': False,
        'is_required': False,
        'is_visible': True,
        'is_editable': True,
        'is_clickable': True,
        'datatype': 'text',
        'form_column': 'COL_1-2',
        'widget_type': 'text_input',
        'label_text': 'URL'
    },
    'note': {
        'is_system_col': False,
        'is_user_key': False,
        'is_required': False,
        'is_visible': True,
        'is_editable': True,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_1-3',
        'widget_type': 'text_area',
        'label_text': 'Note'
    },

    # Col_2
    'id': {
        'is_system_col': True,
        'is_user_key': False,
        'is_required': True,
        'is_visible': True,
        'is_editable': False,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_2-1',
        'widget_type': 'text_input',
        'label_text': 'ID'
    },
    'note_type': {
        'is_system_col': False,
        'is_user_key': False,
        'is_required': False,
        'is_visible': True,
        'is_editable': True,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_2-2',
        'widget_type': 'selectbox',
        'label_text': 'Note Type'
    },
    'tags': {
        'is_system_col': False,
        'is_user_key': False,
        'is_required': False,
        'is_visible': True,
        'is_editable': True,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_2-3',
        'widget_type': 'text_input',
        'label_text': 'Tags'
    },
    'is_active': {
        'is_system_col': False,
        'is_user_key': False,
        'is_required': False,
        'is_visible': False,
        'is_editable': True,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_2-4',
        'widget_type': 'selectbox',
        'label_text': 'Active?'
    },

    'updated_at': {
        'is_system_col': False,
        'is_user_key': False,
        'is_required': False,
        'is_visible': True,
        'is_editable': False,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_2-5',
        'widget_type': 'text_input',
        'label_text': 'Updated At'
    },
    'updated_by': {
        'is_system_col': False,
        'is_user_key': False,
        'is_required': True,
        'is_visible': False,
        'is_editable': False,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_2-6',
        'widget_type': 'text_input',
        'label_text': 'UserID'
    },
    'created_by': {
        'is_system_col': False,
        'is_user_key': False,
        'is_required': True,
        'is_visible': False,
        'is_editable': False,
        'is_clickable': False,
        'datatype': 'text',
        'form_column': 'COL_2-6',
        'widget_type': 'text_input',
        'label_text': 'UserID'
    },
   
}, 

}