# import streamlit as st
# import pandas as pd
# from io import BytesIO

# st.set_page_config(page_title="Overstock Control System", layout="wide")

# st.title("💎 Diamond Overstock Prevention System")

# # -----------------------------
# # FILE UPLOAD
# # -----------------------------
# master_file = st.file_uploader("Upload Master File", type=["xlsx"])
# selection_file = st.file_uploader("Upload Party File (All Stones Selected)", type=["xlsx"])

# # -----------------------------
# # MAIN LOGIC
# # -----------------------------
# if master_file and selection_file:

#     master_df = pd.read_excel(master_file)
#     selection_df = pd.read_excel(selection_file)

#     # Clean column names
#     master_df.columns = master_df.columns.str.strip()
#     selection_df.columns = selection_df.columns.str.strip()

#     # Rename for safety
#     selection_df.rename(columns={
#         "SHAPE": "Shape",
#         "COLOR": "Color",
#         "CLARITY": "Clarity",
#         "CARATS": "Carats"
#     }, inplace=True)

#     # -----------------------------
#     # MATCH + COUNT LOGIC
#     # -----------------------------
#     selected_list = []

#     for i, sel in selection_df.iterrows():
#         for j, mst in master_df.iterrows():

#             if (
#                 sel['Shape'] == mst['Shape'] and
#                 sel['Color'] == mst['Color'] and
#                 sel['Clarity'] == mst['Clarity'] and
#                 mst['From Size'] <= sel['Carats'] <= mst['To Size']
#             ):
#                 selected_list.append(j)

#     # Count selected per row
#     selected_count = pd.Series(selected_list).value_counts()

#     master_df['Selected Qty'] = master_df.index.map(selected_count).fillna(0)

#     # -----------------------------
#     # UPDATE AVAILABLE
#     # -----------------------------
#     master_df['New Available'] = master_df['Available'] - master_df['Selected Qty']

#     # -----------------------------
#     # STATUS
#     # -----------------------------
#     def status(x):
#         if x < 0:
#             return "OVERSTOCK ❌"
#         elif x < 2:
#             return "LOW STOCK ⚠"
#         else:
#             return "OK ✅"

#     master_df['Status'] = master_df['New Available'].apply(status)

#     # -----------------------------
#     # HIGHLIGHT FUNCTION
#     # -----------------------------
#     def highlight(row):
#         if row['New Available'] < 0:
#             return ['background-color:#8B0000; color:white'] * len(row)
#         elif row['New Available'] < 2:
#             return ['background-color:yellow'] * len(row)
#         elif row['Selected Qty'] > 0:
#             return ['background-color:lightblue'] * len(row)
#         else:
#             return [''] * len(row)

#     styled_df = master_df.style.apply(highlight, axis=1)

#     # -----------------------------
#     # SHOW TABLE
#     # -----------------------------
#     st.subheader("📊 Updated Master Stock")
#     st.dataframe(styled_df, use_container_width=True)

#     # -----------------------------
#     # ERROR CHECK
#     # -----------------------------
#     if (master_df['New Available'] < 0).any():
#         st.error("❌ Overstock detected! Please reduce selection.")

#     # -----------------------------
#     # DOWNLOAD EXCEL WITH COLOR
#     # -----------------------------
#     def to_excel(df):
#         output = BytesIO()

#         with pd.ExcelWriter(output, engine='openpyxl') as writer:
#             df.to_excel(writer, index=False, sheet_name='Updated')

#             ws = writer.sheets['Updated']

#             from openpyxl.styles import PatternFill

#             red = PatternFill(start_color="8B0000", end_color="8B0000", fill_type="solid")
#             yellow = PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid")
#             blue = PatternFill(start_color="ADD8E6", end_color="ADD8E6", fill_type="solid")

#             for i, row in df.iterrows():
#                 for col in range(1, len(df.columns)+1):

#                     cell = ws.cell(row=i+2, column=col)

#                     if row['New Available'] < 0:
#                         cell.fill = red
#                     elif row['New Available'] < 2:
#                         cell.fill = yellow
#                     elif row['Selected Qty'] > 0:
#                         cell.fill = blue

#         return output.getvalue()

#     st.download_button(
#         "⬇ Download Updated Master File",
#         data=to_excel(master_df),
#         file_name="updated_master.xlsx"
#     )

# # -----------------------------
# # INSTRUCTIONS
# # -----------------------------
# else:
#     st.info("👆 Upload both Master and Party file to start")

import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Diamond Stock Updater", page_icon="💎", layout="wide")

# ── Size Group from Carats ────────────────────────────────────────────────────
def get_size_group(carats):
    c = float(carats)
    if c <= 0.29:  return "NA"
    if c <= 0.49:  return "0.30 - 0.49"
    if c <= 0.59:  return "0.50 - 0.59"
    if c <= 0.69:  return "0.60 - 0.69"
    if c <= 0.79:  return "0.70 - 0.79"
    if c <= 0.89:  return "0.80 - 0.89"
    if c <= 0.94:  return "0.90 - 0.94"
    if c <= 0.99:  return "0.95 - 0.99"
    if c <= 1.10:  return "1.00 - 1.10"
    if c <= 1.19:  return "1.11 - 1.19"
    if c <= 1.29:  return "1.20 - 1.29"
    if c <= 1.39:  return "1.30 - 1.39"
    if c <= 1.49:  return "1.40 - 1.49"
    if c <= 1.59:  return "1.50 - 1.59"
    if c <= 1.69:  return "1.60 - 1.69"
    if c <= 1.79:  return "1.70 - 1.79"
    if c <= 1.89:  return "1.80 - 1.89"
    if c <= 1.99:  return "1.90 - 1.99"
    if c <= 2.10:  return "2.00 - 2.10"
    if c <= 2.49:  return "2.11 - 2.49"
    if c <= 2.59:  return "2.50 - 2.59"
    if c <= 2.99:  return "2.60 - 2.99"
    if c <= 3.10:  return "3.00 - 3.10"
    if c <= 3.49:  return "3.11 - 3.49"
    if c <= 3.59:  return "3.50 - 3.59"
    if c <= 3.99:  return "3.60 - 3.99"
    if c <= 4.10:  return "4.00 - 4.10"
    if c <= 4.49:  return "NA"
    if c <= 4.59:  return "4.50 - 4.59"
    if c <= 4.99:  return "NA"
    if c <= 5.10:  return "5.00 - 5.10"
    if c <= 5.49:  return "NA"
    if c <= 5.59:  return "5.50 - 5.59"
    if c <= 5.99:  return "NA"
    if c <= 6.10:  return "6.00 - 6.10"
    if c <= 6.49:  return "NA"
    if c <= 6.59:  return "6.50 - 6.59"
    if c <= 6.99:  return "NA"
    if c <= 7.10:  return "7.00 - 7.10"
    if c <= 7.99:  return "NA"
    if c <= 8.10:  return "8.00 - 8.10"
    if c <= 8.99:  return "NA"
    if c <= 9.10:  return "9.00 - 9.10"
    if c <= 9.99:  return "NA"
    if c <= 10.10: return "10.00 - 10.10"
    if c <= 10.99: return "NA"
    if c <= 11.10: return "11.00 - 11.10"
    if c <= 11.99: return "NA"
    if c <= 12.10: return "12.00 - 12.10"
    if c <= 12.99: return "NA"
    if c <= 13.10: return "13.00 - 13.10"
    if c <= 13.99: return "NA"
    if c <= 14.10: return "14.00 - 14.10"
    if c <= 14.99: return "NA"
    if c <= 15.10: return "15.00 - 15.10"
    if c <= 19.99: return "NA"
    if c <= 21.99: return "20.00 - 21.99"
    return "NA"

def build_key(shape, size_group, color, clarity):
    return f"{str(shape).strip()}{str(size_group).strip()}{str(color).strip()}{str(clarity).strip()}"

def to_excel_bytes(df, sheet_name):
    buf = BytesIO()
    with pd.ExcelWriter(buf, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=False)
    return buf.getvalue()

def process(master_file, selection_file):
    # ── Load Master ──────────────────────────────────────────────────────────
    master_xl = pd.read_excel(master_file, sheet_name=None)
    sheet_name = list(master_xl.keys())[0]
    master = master_xl[sheet_name].copy()

    master['Available'] = pd.to_numeric(master['Available'], errors='coerce').fillna(0).astype(int)
    master['Grid']      = pd.to_numeric(master['Grid'],      errors='coerce').fillna(0).astype(int)

    master['_key'] = master.apply(
        lambda r: build_key(r['Shape'], r['Sixe Group'], r['Color'], r['Clarity']), axis=1
    )

    # ── Load Selection - only SELECTED rows ──────────────────────────────────
    sel = pd.read_excel(selection_file)
    selected = sel[sel['SELECTION'].astype(str).str.strip().str.upper() == 'SELECTED'].copy()

    if selected.empty:
        return master.drop(columns=['_key']), [], [], [], sheet_name, 0

    selected['_size_group'] = selected['CARATS'].apply(get_size_group)
    selected['_shape'] = (
        selected['ACTUAL SHAPE'].fillna(selected['SHAPE'])
        .astype(str).str.strip().str.upper()
    )
    selected['_key'] = selected.apply(
        lambda r: build_key(r['_shape'], r['_size_group'], r['COLOR'], r['CLARITY']), axis=1
    )

    sel_counts = selected.groupby('_key').size().to_dict()

    # ── Update Logic ─────────────────────────────────────────────────────────
    # Grid     = Target / Min stones required
    # Available = Stones we already have in stock
    #
    # Rule: Only update if Available < Grid (we are understocked)
    #       If Available >= Grid → already have enough → SKIP (avoid overstock)
    #       New Available = Old Available + Selected Count
    # ─────────────────────────────────────────────────────────────────────────
    updated   = []   # rows where available was updated
    skipped_overstock = []   # rows ignored because already at/above grid
    not_found = []   # keys from selection not in master

    for key, sel_count in sel_counts.items():
        mask = master['_key'] == key
        if not mask.any():
            not_found.append({'Key': key, 'Selected Count': sel_count, 'Reason': 'Key not found in master'})
            continue

        for idx in master[mask].index:
            grid      = int(master.at[idx, 'Grid'])
            old_avail = int(master.at[idx, 'Available'])
            shape     = master.at[idx, 'Shape']
            size_grp  = master.at[idx, 'Sixe Group']
            color     = master.at[idx, 'Color']
            clarity   = master.at[idx, 'Clarity']

            # ── CORE RULE ────────────────────────────────────────────────────
            if old_avail >= grid:
                # Already have enough stock — do NOT add → prevents overstock
                skipped_overstock.append({
                    'Shape': shape, 'Size Group': size_grp,
                    'Color': color, 'Clarity': clarity,
                    'Grid (Need)': grid,
                    'Available (Have)': old_avail,
                    'Selected Count': sel_count,
                    'Reason': f'Already stocked ({old_avail} ≥ Grid {grid}) — SKIPPED'
                })
            else:
                # Understocked → add selected stones to available
                new_avail = old_avail + sel_count
                master.at[idx, 'Available'] = new_avail
                updated.append({
                    'Shape': shape, 'Size Group': size_grp,
                    'Color': color, 'Clarity': clarity,
                    'Grid (Need)': grid,
                    'Old Available': old_avail,
                    'Selected Added': sel_count,
                    'New Available': new_avail,
                })

    master.drop(columns=['_key'], inplace=True)
    return master, updated, skipped_overstock, not_found, sheet_name, len(selected)


# ── UI ────────────────────────────────────────────────────────────────────────
st.title("💎 Diamond Stock Auto-Updater")
st.caption("Prevents overstock — only updates Available when we need more stones (Available < Grid)")

st.divider()

col1, col2 = st.columns(2)
with col1:
    master_file = st.file_uploader("📂 Master File (.xlsx)", type=["xlsx"])
with col2:
    selection_file = st.file_uploader("📂 Selection File (.xlsx)", type=["xlsx"])

if master_file and selection_file:
    with st.spinner("Processing…"):
        master_updated, updated, skipped_os, not_found, sheet_name, total_sel = process(
            master_file, selection_file
        )

    st.divider()

    # ── Metrics ───────────────────────────────────────────────────────────────
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Master Rows",           len(master_updated))
    c2.metric("Total Selected Stones", total_sel)
    c3.metric("✅ Rows Updated",       len(updated))
    c4.metric("⏭️ Skipped (Overstock)", len(skipped_os))
    c5.metric("❌ Key Not Found",      len(not_found))

    st.divider()

    # ── Updated Rows ──────────────────────────────────────────────────────────
    st.subheader("✅ Updated Rows  —  Available was Understocked")
    st.markdown("""
    > **Rule:** `Available < Grid` → We need more stones → **New Available = Old Available + Selected Added**
    """)

    if updated:
        df_up = pd.DataFrame(updated)

        def highlight_updated(row):
            styles = [''] * len(row)
            cols = list(df_up.columns)
            if 'Selected Added' in cols:
                styles[cols.index('Selected Added')] = 'background-color:#14532d;color:#86efac'
            if 'New Available' in cols:
                styles[cols.index('New Available')]  = 'background-color:#1e3a5f;color:#93c5fd;font-weight:bold'
            return styles

        st.dataframe(df_up.style.apply(highlight_updated, axis=1), use_container_width=True, hide_index=True)
    else:
        st.info("No rows needed updating.")

    st.divider()

    # ── Skipped Overstock ─────────────────────────────────────────────────────
    st.subheader("⏭️ Skipped Rows  —  Already Sufficiently Stocked")
    st.markdown("""
    > **Rule:** `Available ≥ Grid` → We already have enough → **No update made (prevents overstock)**
    """)

    if skipped_os:
        df_sk = pd.DataFrame(skipped_os)

        def highlight_skipped(row):
            styles = [''] * len(row)
            cols = list(df_sk.columns)
            if 'Reason' in cols:
                styles[cols.index('Reason')] = 'background-color:#422006;color:#fbbf24'
            return styles

        st.dataframe(df_sk.style.apply(highlight_skipped, axis=1), use_container_width=True, hide_index=True)
    else:
        st.info("No overstock rows found.")

    # ── Not Found ─────────────────────────────────────────────────────────────
    if not_found:
        with st.expander(f"❌  {len(not_found)} Key(s) from Selection NOT Found in Master"):
            st.dataframe(pd.DataFrame(not_found), use_container_width=True, hide_index=True)

    st.divider()

    # ── Preview ───────────────────────────────────────────────────────────────
    st.subheader("📋 Updated Master File Preview")
    st.dataframe(master_updated.head(200), use_container_width=True, hide_index=True)

    st.download_button(
        label="⬇️  Download Updated Master File (.xlsx)",
        data=to_excel_bytes(master_updated, sheet_name),
        file_name="Updated_Master_File.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
        type="primary",
    )

elif master_file or selection_file:
    st.info("Please upload **both** files to proceed.")
else:
    st.markdown("""
    ### 📌 Logic Explained

    | Condition | Action |
    |-----------|--------|
    | `Available < Grid` | ✅ **Update** → New Available = Old Available + Selected Count |
    | `Available ≥ Grid` | ⏭️ **Skip** → Already enough stock, do NOT add (prevents overstock) |
    | Key not in master  | ❌ **Not found** → Logged separately |

    ---
    ### Examples

    | Grid (Need) | Available (Have) | Selected | Result |
    |-------------|-----------------|----------|--------|
    | 2 | 3 | 5 | ⏭️ **SKIP** — already have 3, only need 2 |
    | 40 | 5 | 20 | ✅ **5 + 20 = 25** — understocked, added |
    | 10 | 10 | 3 | ⏭️ **SKIP** — exactly at grid, no need |
    | 15 | 8 | 6 | ✅ **8 + 6 = 14** — understocked, added |
    """)