<template>
  <div id="admin-page" :class="{ 'has-background-dark': isDarkMode }">
    <!-- Header -->
    <nav
      class="navbar is-primary"
      role="navigation"
      aria-label="main navigation"
    >
      <div class="navbar-brand">
        <a class="navbar-item">
          <h1 class="title">Admin Dashboard</h1>
        </a>
      </div>
      <div class="navbar-end">
        <div class="navbar-item">
          <button class="button" @click="toggleDarkMode">
            {{ isDarkMode ? "🌞 Light Mode" : "🌙 Dark Mode" }}
          </button>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <div class="columns">
      <!-- Sidebar -->
      <aside class="column is-one-quarter menu">
        <h1 class="menu-label">Database Tables</h1>
        <ul class="menu-list">
          <li v-for="table in tables" :key="table">
            <a
              @click="fetchTableRecords(table)"
              :class="{
                'is-active': selectedTable === table,
              }"
            >
              {{ table.replace(/_/g, "").toUpperCase() }}
            </a>
          </li>
        </ul>
      </aside>

      <!-- Content Section -->
      <section class="column">
        <div v-if="loading" class="has-text-centered">
          <button class="button is-loading is-large is-text">Loading</button>
        </div>
        <div v-else-if="records.length > 0">
          <div class="level">
            <div class="level-left">
              <h2 class="title is-4">Records in Table: {{ selectedTable }}</h2>
            </div>
            <div class="level-right">
              <div class="field has-addons">
                <div class="control">
                  <input
                    class="input"
                    type="text"
                    v-model="searchQuery"
                    placeholder="Search records..."
                    @input="applyFilters"
                  />
                </div>
                <div class="control">
                  <button class="button is-primary" @click="openModal('add')">
                    Add
                  </button>
                </div>
                <div class="control">
                  <button
                    class="button is-warning"
                    @click="openModal('edit')"
                    :disabled="!selectedRecord"
                  >
                    Edit
                  </button>
                </div>
                <div class="control">
                  <button
                    class="button is-danger"
                    @click="openDeleteModal"
                    :disabled="!selectedRecord"
                  >
                    Delete
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Records Table -->
          <div class="table-container">
            <table class="table is-fullwidth is-striped is-hoverable">
              <thead>
                <tr>
                  <th v-for="(value, key) in records[0]" :key="key">
                    {{ key }}
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="record in filteredRecords"
                  :key="record.id"
                  @click="selectRecord(record)"
                  :class="{ 'is-selected': record === selectedRecord }"
                >
                  <td v-for="(value, key) in record" :key="key">{{ value }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        <div v-else-if="selectedTable && records.length === 0">
          <p class="has-text-centered">
            No records found for the selected table.
          </p>
        </div>
        <div v-else>
          <p class="has-text-centered">Select a table to view its records.</p>
        </div>
      </section>
    </div>

    <!-- Add/Edit Modal -->
    <div
      :style="{ visibility: isModalVisible ? 'visible' : 'hidden' }"
      class="modal modalOverlay1"
      :class="{ 'is-active': showModal }"
    >
      <div class="modal-background" @click="closeModal"></div>
      <div class="modal-card">
        <header class="modal-card-head">
          <p class="modal-card-title">
            {{
              modalType === "add" ? "Add New Record" : "Edit Record from here "
            }}
          </p>
          <button
            class="delete"
            aria-label="close"
            @click="closeModal"
          ></button>
        </header>
        <section class="modal-card-body">
          <form @submit.prevent="handleSubmit">
            <div v-for="(value, key) in modalRecord" :key="key" class="field">
              <label class="label">{{ key }}</label>
              <div class="control">
                <input
                  class="input"
                  type="text"
                  :id="key"
                  v-model="modalRecord[key]"
                  :disabled="key === 'id' && modalType === 'edit'"
                  :placeholder="'Enter ' + key"
                />
              </div>
            </div>
          </form>
        </section>
        <footer class="modal-card-foot">
          <button class="button is-success" @click="handleSubmit">Save</button>
          <button class="button" @click="closeModal">Cancel</button>
        </footer>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div
      :style="{ visibility: isDeleteModalVisible ? 'visible' : 'hidden' }"
      class="modal modalOverlayDelete"
      :class="{ 'is-active': showDeleteModal }"
    >
      <div class="modal-background" @click="closeDeleteModal"></div>
      <div class="modal-card">
        <header class="modal-card-head">
          <p class="modal-card-title">Delete Record</p>
          <button
            class="delete"
            aria-label="close"
            @click="closeDeleteModal"
          ></button>
        </header>
        <section class="modal-card-body">
          <p>Are you sure you want to delete this record?</p>
        </section>
        <footer class="modal-card-foot">
          <button class="button is-danger" @click="confirmDelete">
            Delete
          </button>
          <button class="button" @click="closeDeleteModal">Cancel</button>
        </footer>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { h } from "vue";

export default {
  data() {
    return {
      tables: [],
      records: [],
      selectedTable: null,
      loading: false,
      selectedRecord: null,
      showModal: false,
      showDeleteModal: false,
      modalType: "",
      modalRecord: {},
      isDarkMode: false,
      searchQuery: "",
      filteredRecords: [],
      isModalVisible: false,
      isDeleteModalVisible: false,
    };
  },
  methods: {
    async fetchTables() {
      this.loading = true;
      try {
        const response = await axios.get("/admin/tables");
        this.tables = response.data.tables;
      } catch (error) {
        console.error("Error fetching tables:", error);
      } finally {
        this.loading = false;
      }
    },
    async fetchTableRecords(table) {
      this.selectedTable = table;
      this.loading = true;
      try {
        const response = await axios.get(`/admin/tables/${table}/records`);
        this.records = response.data.records;
        this.filteredRecords = this.records;
      } catch (error) {
        console.error(`Error fetching records for table ${table}:`, error);
      } finally {
        this.loading = false;
      }
    },
    selectRecord(record) {
      this.selectedRecord = record;
    },
    openModal(type) {
      this.modalType = type;
      this.showModal = true;
      this.isModalVisible = true;

      if (type === "edit") {
        this.modalRecord = type === "edit" && this.selectedRecord;
      } else if (type === "add") {
        this.modalRecord = this.initializeEmptyRecord(type);
      }
      this.initializeEmptyRecord();
    },
    initializeEmptyRecord(type = "add") {
      const emptyRecord = {};
      if (this.records.length > 0) {
        Object.keys(this.records[0]).forEach((key) => {
          emptyRecord[key] = "";
        });
        if (type === "add") {
          delete emptyRecord.id;
        }
      }
      return this.getSortedKeys(emptyRecord);
    },
    getSortedKeys(obj) {
      return Object.keys(obj)
        .sort()
        .reduce((acc, key) => {
          acc[key] = obj[key];
          return acc;
        }, {});
    },

    closeModal() {
      this.showModal = false;
      this.isModalVisible = false;
    },
    openDeleteModal() {
      if (this.selectedRecord) {
        this.showDeleteModal = true;
        this.isDeleteModalVisible = true;
      }
    },
    closeDeleteModal() {
      this.showDeleteModal = false;
      this.isDeleteModalVisible = false;
    },
    toggleDarkMode() {
      this.isDarkMode = !this.isDarkMode;
    },
    applyFilters() {
      this.filteredRecords = this.records.filter((record) =>
        Object.values(record).some((value) =>
          String(value).toLowerCase().includes(this.searchQuery.toLowerCase())
        )
      );
    },
    async handleSubmit() {
      try {
        if (this.modalType === "add") {
          const response = await axios.post(
            `/admin/tables/${this.selectedTable}/records`,
            this.modalRecord
          );
          this.records.push(response.data);
        } else if (this.modalType === "edit") {
          const response = await axios.put(
            `/admin/tables/${this.selectedTable}/records/${this.modalRecord.id}`,
            this.modalRecord
          );
          this.records = this.records.map((record) =>
            record.id === response.data.id ? response.data : record
          );
        }
        this.filteredRecords = [...this.records];
        this.closeModal();
      } catch (error) {
        console.error("Error saving record:", error);
      }
    },
    async confirmDelete() {
      if (!this.selectedRecord) return;
      try {
        await axios.delete(
          `/admin/tables/${this.selectedTable}/records/${this.selectedRecord.id}`
        );
        this.records = this.records.filter(
          (record) => record.id !== this.selectedRecord.id
        );
        this.filteredRecords = this.records;
        this.selectedRecord = null;
        this.closeDeleteModal();
      } catch (error) {
        console.error("Error deleting record:", error);
      }
    },
  },
  mounted() {
    this.fetchTables();
  },
};
</script>

<style scoped>
body {
  margin: 0;
  font-family: "Arial", sans-serif;
  background-color: #f9f9f9;
  color: #333;
}

.header {
  background-color: #4caf50;
  color: white;
  padding: 1rem 2rem;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.main {
  display: flex;
  flex: 1;
  overflow: hidden;
}

.sidebar {
  background-color: #ffffff;
  width: 300px;
  padding: 1rem;
  border-right: 1px solid #ddd;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.05);
  overflow-y: auto;
}

.table-list li {
  padding: 10px;
  cursor: pointer;
  border-bottom: 1px solid #ddd;
}

.table-list li.active {
  background-color: #4caf50;
  color: white;
}

.content {
  flex: 1;
  padding: 2rem;
  overflow-y: auto;
  background-color: #f7f7f7;
}

.content-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.styled-table {
  width: 100%;
  border-collapse: collapse;
  background: white;
}

.styled-table th {
  background-color: #4caf50;
  color: white;
  padding: 12px 15px;
  text-align: left;
  border: 1px solid #ddd;
}

.styled-table td {
  padding: 12px 15px;
  border: 1px solid #ddd;
}

.styled-table tbody tr:nth-child(even) {
  background-color: #f3f3f3;
}

.styled-table tbody tr:hover {
  background-color: #f1f1f1;
}

.styled-table tbody tr.selected {
  background-color: #e8f5e9;
}

.styled-table th,
.styled-table td {
  transition: background-color 0.3s ease;
}

.loader {
  text-align: center;
  font-size: 1.2rem;
  color: #666;
}

.btn {
  font-size: 1rem;
  border: none;
  padding: 0.5rem 1rem;
  margin: 0 5px;
  cursor: pointer;
  border-radius: 5px;
}

.btn-add {
  background-color: #4caf50;
  color: white;
}

.btn-update {
  background-color: #ffc107;
  color: white;
}

.btn-delete {
  background-color: #f44336;
  color: white;
}

.btn:hover {
  opacity: 0.9;
}

/* Add same styles from previous version */
.modal {
  background: white;
  padding: 20px;
  border-radius: 10px;
  width: 400px;
  max-width: 90%;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.modal h2 {
  margin-top: 0;
}

.modal .form-group {
  margin-bottom: 15px;
}

.modal .form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.modal .form-group input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 5px;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.modal-actions .btn {
  padding: 8px 15px;
  border-radius: 5px;
}

.modal-actions .btn-save {
  background-color: #4caf50;
  color: white;
  border: none;
}

.modal-actions .btn-cancel {
  background-color: #f44336;
  color: white;
  border: none;
}

.modal-actions .btn:hover {
  opacity: 0.9;
}

body {
  font-family: "Roboto", sans-serif;
  margin: 0;
  background-color: var(--background-color);
  color: var(--text-color);
  transition: background-color 0.3s ease, color 0.3s ease;
}

/* Dark Mode Variables */
.dark {
  --background-color: #121212;
  --text-color: #ffffff;
  --card-bg: #1e1e1e;
}

.light {
  --background-color: #f9f9f9;
  --text-color: #333;
  --card-bg: #fff;
}

/* Futuristic Glassmorphism Modal */
.modalOverlay1,
.modalOverlayDelete {
  visibility: hidden;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  backdrop-filter: blur(10px);
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  animation: fadeIn 0.5s ease-out;
}

.modal.futuristic-modal {
  position: relative;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(20px);
  padding: 20px;
  width: 400px;
  max-width: 90%;
  border-radius: 15px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.37);
  color: var(--text-color);
  animation: slideIn 0.4s ease-out;
  overflow: hidden;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 15px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

.modal-header h2 {
  font-size: 1.5em;
  font-weight: 600;
  margin: 0;
}

.close-btn {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: var(--text-color);
  font-size: 1.2em;
  padding: 5px;
  cursor: pointer;
  border-radius: 50%;
  transition: transform 0.2s ease-in;
}

.close-btn:hover {
  transform: scale(1.2);
  background: rgba(255, 255, 255, 0.3);
}

.modal-form {
  margin-top: 15px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.8);
}

.form-group input {
  width: 100%;
  padding: 10px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.2);
  color: var(--text-color);
  outline: none;
  transition: box-shadow 0.2s ease-in;
}

.form-group input:focus {
  box-shadow: 0 0 8px rgba(255, 255, 255, 0.8);
  border-color: rgba(255, 255, 255, 0.5);
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 15px;
}

.modal-actions .btn {
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
  transition: transform 0.2s ease-in, box-shadow 0.2s ease-in;
}

.modal-actions .btn-save {
  background: linear-gradient(45deg, #4caf50, #81c784);
  color: white;
}

.modal-actions .btn-cancel {
  background: linear-gradient(45deg, #f44336, #e57373);
  color: white;
}

.modal-actions .btn:hover {
  transform: scale(1.1);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
}

/* Animations */
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes slideIn {
  from {
    transform: translateY(-50px);
  }
  to {
    transform: translateY(0);
  }
}
</style>
