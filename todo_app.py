import streamlit as st
import json
import os

FILE_PATH = "tasks.json"

# Fungsi untuk memuat data dari file
def load_tasks():
    if os.path.exists(FILE_PATH):
        try:
            with open(FILE_PATH, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []

# Fungsi untuk menyimpan data ke file
def save_tasks(tasks):
    with open(FILE_PATH, "w") as f:
        json.dump(tasks, f)

# Inisialisasi session_state
if "tasks" not in st.session_state:
    st.session_state.tasks = load_tasks()
# Inisialisasi variabel edit
if "tugas_diedit" not in st.session_state:
    st.session_state.tugas_diedit = None


st.title("📝 To-Do List")

# Input tugas baru
with st.form("tugas_form"):
    new_task = st.text_input("Masukkan tugas baru")
    kategori = st.selectbox("Pilih kategori", ["Belajar", "Kerja", "Pribadi"])
    prioritas = st.selectbox("Pilih prioritas", ["Rendah", "Sedang", "Tinggi"])
    deadline = st.date_input("Tentukan deadline (opsional)")
    submitted = st.form_submit_button("Tambah Tugas")

    if submitted:
        if new_task:
            new_task_data = {
                "tugas": new_task,
                "kategori": kategori,
                "prioritas": prioritas,
                "deadline": str(deadline),
                "selesai": False
            }
            st.session_state.tasks.append(new_task_data)
            save_tasks(st.session_state.tasks)
            st.success(f"Tugas '{new_task}' berhasil ditambahkan.")
        else:
            st.warning("Tugas tidak boleh kosong.")

# Filter kategori
kategori_filter = st.selectbox(
    "Filter berdasarkan kategori",
    options=["Semua"] + list({t["kategori"] for t in st.session_state.tasks})
)

# Filter tugas
if kategori_filter == "Semua":
    filtered_tasks = st.session_state.tasks
else:
    filtered_tasks = [t for t in st.session_state.tasks if t["kategori"] == kategori_filter]

# Urutkan berdasarkan prioritas (opsional)
prioritas_urutan = {"Tinggi": 0, "Sedang": 1, "Rendah": 2}
filtered_tasks.sort(key=lambda x: prioritas_urutan.get(x.get("prioritas", "Sedang"), 3))


# Tampilkan daftar tugas
st.subheader(f"Daftar Tugas - Kategori: {kategori_filter}")
if filtered_tasks:
    updated = False
    for i, task in enumerate(filtered_tasks):
        idx_global = st.session_state.tasks.index(task)##
        col1, col2, col3 = st.columns([0.7, 0.15, 0.15])
        ##col1, col2 = st.columns([0.85, 0.15])
        deadline_str = task['deadline'] if isinstance(task['deadline'], str) else str(task['deadline'])
        label = f" {task.get('tugas', 'Tanpa Nama')} | Prioritas: {task.get('prioritas', 'Tidak Ditentukan')} (Deadline: {deadline_str})"

        selesai = col1.checkbox(label, value=task["selesai"], key=f"selesai_{idx_global}")
        ##selesai = col1.checkbox(label, value=task["selesai"], key=f"selesai_{i}")
        if selesai != task["selesai"]:
            task["selesai"] = selesai
            updated = True

        ##if selesai != task["selesai"]:
            ##task["selesai"] = selesai
            ##updated = True

        if col2.button("Edit", key=f"edit_{i}"):
            st.session_state.tugas_diedit = task
            st.session_state.index_diedit = idx_global
            st.rerun()

        if col3.button("Hapus", key=f"delete_{i}"):
            st.session_state.tugas_dihapus = task
            st.session_state.konfirmasi_hapus = True
            st.rerun()

        ##if col2.button("Hapus", key=f"delete_{i}"):
            ##st.session_state.tugas_dihapus = task
            ##st.session_state.konfirmasi_hapus = True
            ##st.rerun()

        # Inisialisasi konfirmasi hapus
        if "konfirmasi_hapus" not in st.session_state:
            st.session_state.konfirmasi_hapus = False
        if "tugas_dihapus" not in st.session_state:
            st.session_state.tugas_dihapus = None


    # Tampilkan dialog konfirmasi jika diperlukan
    if st.session_state.konfirmasi_hapus and st.session_state.tugas_dihapus:
        st.warning(f"Apakah kamu yakin ingin menghapus tugas: '{st.session_state.tugas_dihapus['tugas']}'?")
        col_confirm, col_cancel = st.columns(2)

        if col_confirm.button("Ya, Hapus"):
            st.session_state.tasks.remove(st.session_state.tugas_dihapus)
            save_tasks(st.session_state.tasks)
            st.session_state.konfirmasi_hapus = False
            st.session_state.tugas_dihapus = None
            st.success("Tugas berhasil dihapus.")
            st.rerun()

        if col_cancel.button("Batal"):
            st.session_state.konfirmasi_hapus = False
            st.session_state.tugas_dihapus = None
            st.rerun()

    # Form edit tugas jika ada tugas yang sedang diedit
    if st.session_state.tugas_diedit:
        st.subheader("✏️ Edit Tugas")
        with st.form("edit_form"):
            tugas_baru = st.text_input("Edit tugas", value=st.session_state.tugas_diedit["tugas"])
            kategori_baru = st.selectbox("Edit kategori", ["Belajar", "Kerja", "Pribadi"],
                                         index=["Belajar", "Kerja", "Pribadi"].index(
                                             st.session_state.tugas_diedit["kategori"]))
            prioritas_baru = st.selectbox("Edit prioritas", ["Rendah", "Sedang", "Tinggi"],
                                          index=["Rendah", "Sedang", "Tinggi"].index(
                                              st.session_state.tugas_diedit["prioritas"]))

            # Ubah deadline dari string ke datetime.date
            import datetime

            try:
                deadline_default = datetime.datetime.strptime(st.session_state.tugas_diedit["deadline"],
                                                              "%Y-%m-%d").date()
            except:
                deadline_default = datetime.date.today()

            deadline_baru = st.date_input("Edit deadline", value=deadline_default)

            # Inilah tombol submit untuk form
            submitted_edit = st.form_submit_button("Simpan Perubahan")

            if submitted_edit:
                # Simpan hasil edit
                st.session_state.tasks[st.session_state.index_diedit] = {
                    "tugas": tugas_baru,
                    "kategori": kategori_baru,
                    "prioritas": prioritas_baru,
                    "deadline": str(deadline_baru),
                    "selesai": st.session_state.tugas_diedit["selesai"]
                }
                save_tasks(st.session_state.tasks)
                st.session_state.tugas_diedit = None
                st.success("Tugas berhasil diperbarui.")
                st.rerun()

    if updated:
        save_tasks(st.session_state.tasks)
else:
    st.info("Tidak ada tugas pada kategori ini.")
