"""
data_editor app built on streamlit and duckdb

data: languages.csv
schema:
name
name_native
code  (2 letters)
description
is_natural (1 - human-spoken, 0 - system-programming)
url
family
branch
is_active
number_speakers
note

sources:
	- https://en.wikipedia.org/wiki/List_of_languages_by_number_of_native_speakers
	- https://github.com/forxer/languages-list/blob/master/src/Languages.csv

Test:
cd projects\wgong
activate_venv_st_latest
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import duckdb
from pathlib import Path 
import shutil
from io import StringIO 

DEBUG_FLAG = False # True



STR_SAVE_DB = "Save DB"
STR_EXPORT_CSV = "Export CSV"

####  Helper functions ==============================================
def rename_file_adding_ts(fn, do_rename=False, do_copy=False):
    """ rename file by adding timestamp, useful for archiving
    eg,
    INPUT_FILENAME = "data/languages.csv"
    output = rename_file_adding_ts(INPUT_FILENAME)
    # WindowsPath('data/languages-20230716_220400.csv')
    """
    p = Path(fn)
    ts = datetime.strftime(datetime.now(),"%Y%m%d_%H%M%S")
    new_fn = p.parent / f"{p.stem}-{ts}{p.suffix}"
    if do_copy:
        shutil.copy(p, new_fn)
    if do_rename:
        p.rename(new_fn)
    return new_fn

def generate_output_sql(df, edited_rows, key_cols, table_name):
	"""generate an SQL to persist changing data from data_editor
	"""
	sql_stmt = []
	# process updates
	updated_rows = edited_rows["edited_rows"]
	for idx in updated_rows.keys():
		row = df.iloc[idx]
		where_clause = []
		for c in key_cols:
			k_v = row.get(c)
			where_clause.append(f" {c} = '{k_v}' ")

		set_clause = []
		v_dic = updated_rows[idx]
		for c in v_dic.keys():
			if c in key_cols: continue  # skip key_cols

			v = v_dic.get(c)
			set_clause.append(f" {c} = '{v}' ")

		sql_upd = f"""
		update {table_name} 
		set {",".join(set_clause)}
		where {",".join(where_clause)};
		"""
		# st.write(f"Update SQL:\n{sql_upd}")
		sql_stmt.append(sql_upd)

	# process deletes
	idx_deleted = edited_rows["deleted_rows"]
	for idx in idx_deleted:
		row = df.iloc[idx]
		where_clause = []
		for c in key_cols:
			k_v = row.get(c)
			where_clause.append(f" {c} = '{k_v}' ")

		sql_del = f"""
		delete from {table_name} 
		where {",".join(where_clause)};
		"""
		# st.write(f"Delete SQL:\n{sql_del}")
		sql_stmt.append(sql_del)

	# process deletes
	rows_inserted = edited_rows["added_rows"]
	for row in rows_inserted:
		cols = []
		vals = []
		for k,v in row.items():
			cols.append(k)
			vals.append(f"'{v}'")

		if not "is_natural" in row:
			cols.append("is_natural")
			vals.append('1')
		if not "is_active" in row:
			cols.append("is_active")
			vals.append('0')

		sql_ins = f"""
		insert into {table_name} ({",".join(cols)})
		values ({",".join(vals)});
		"""
		# st.write(f"Insert SQL:\n{sql_ins}")
		sql_stmt.append(sql_ins)

	return "\n".join(sql_stmt) if sql_stmt else ""

def convert_df2csv(df, index=True):
    return df.to_csv(index=index).encode('utf-8')

# st.write(f"DuckDB version: {duckdb.__version__}")
####=========================================================
DB_FILENAME = "wg_data_editor.duckdb"
conn = duckdb.connect(DB_FILENAME)

st.header(f"Streamlit Data Editor")

def main():
	df = None
	INPUT_FILENAME = ""
	TABLE_NAME = ""

	c_left, c_right = st.columns([4,4])

	with c_right:
		st.markdown("""#### <span style="color:green">Upload CSV file</span>""", unsafe_allow_html=True)
		txt_file = st.file_uploader("Upload", key="upload_txt")
		if txt_file is not None:
			csv_io = StringIO(txt_file.getvalue().decode("utf-8"))
			df = pd.read_csv(csv_io)
			INPUT_FILENAME = txt_file.name
			TABLE_NAME = (Path(INPUT_FILENAME).stem).lower()
			KEY_NAME_DATA_EDITOR = f"df_{TABLE_NAME}"

			#  CREATE TABLE {TABLE_NAME} AS select * from read_csv_auto('{p}');
			try: 
				conn.execute(f"select count(*) from {TABLE_NAME}")
			except Exception as e:
				# print(str(e))
				if "Catalog Error: Table" in str(e):
					conn.execute(f"""
					CREATE TABLE {TABLE_NAME} AS SELECT * FROM df
					""")

			df = conn.execute(f"select * from {TABLE_NAME}").fetchdf()
			# st.session_state["TABLE_NAME"] = TABLE_NAME

	with c_left:
		st.markdown(f"""#### <span style="color:blue">Input</span>
- CSV file: {INPUT_FILENAME}
- Table name: {TABLE_NAME}
	    """, unsafe_allow_html=True)

	# read data
	# df = pd.read_csv(INPUT_FILENAME)

	if df is None:
		return

	df_cols = list(df.columns)
	key_cols = st.multiselect(
		"Select key columns", 
		df_cols,
		df_cols[:1]
	)
	# st.write(f"key columns = {key_cols}")
	column_config = {}
	for col in key_cols:
		column_config.update({
				col: st.column_config.Column(
					col,
					# disabled =True,
					help="Key column, don't edit",
					required =True,
			)})
	for col in df_cols:
		if col in column_config: continue
		if col.lower().startswith("url") or col.lower().endswith("url"):
			column_config.update({
					col: st.column_config.LinkColumn(
						col,
						help="Link column, double-click to browse",
				)})
	# st.write(column_config)

	# display df in data_editor
	edited_df = st.data_editor(
			df, 
			column_config=column_config,
			key=KEY_NAME_DATA_EDITOR, 
			num_rows="dynamic", 
			hide_index=False)

	edited_rows = st.session_state[KEY_NAME_DATA_EDITOR]
	sql_stmt = generate_output_sql(df, edited_rows, key_cols, table_name=TABLE_NAME)

	# handle buttons
	btn_c1, btn_c2, _ = st.columns([3,3, 5])
	with btn_c1:
		btn_save = st.button(STR_SAVE_DB)
		if btn_save:
			conn.sql(sql_stmt)
			conn.commit()

	with btn_c2:
		df = conn.execute(f"select * from {TABLE_NAME}").fetchdf()
		new_fn = rename_file_adding_ts(INPUT_FILENAME)
		st.download_button(
			label=STR_EXPORT_CSV,
			data=convert_df2csv(df, index=False),
			file_name=new_fn.name,
			mime='text/csv',
		)

	# debug
	if DEBUG_FLAG:
		c1, c2 = st.columns([3,5])
		with c2:
			st.subheader("Edited df")
			st.write(edited_df)

		with c1:
			st.subheader("Edited rows")
			st.write(edited_rows)

		st.subheader("Output SQL")
		st.write(sql_stmt)


	# close DB
	conn.close()


if __name__ == "__main__":
    main()