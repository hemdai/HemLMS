<template>
  <div id="admin-page">
    <!-- Header -->
    <header class="header">
      <h1>Admin Dashboard</h1>
    </header>

    <!-- Main Content -->
    <main class="main">
      <aside class="sidebar">
        <h2>Database Tables</h2>
        <ul class="table-list">
          <li
            v-for="table in tables"
            :key="table"
            @click="fetchTableRecords(table)"
            :class="{ active: selectedTable === table }"
          >
            {{ table }}
          </li>
        </ul>
      </aside>

      <section class="content">
        <div v-if="loading" class="loader">Loading...</div>

        <div v-else-if="records.length > 0">
          <div class="content-header">
            <h2>Records in Table: {{ selectedTable }}</h2>
            <div class="action-buttons">
              <button
                @click="openModal('add')"
                class="btn btn-add"
                title="Add Record"
              >
                ➕
              </button>
              <button
                @click="openModal('edit')"
                class="btn btn-update"
                title="Edit Selected Record"
                :disabled="!selectedRecord"
              >
                ✏️
              </button>
              <button
                @click="deleteRecord"
                class="btn btn-delete"
                title="Delete Selected Record"
                :disabled="!selectedRecord"
              >
                ❌
              </button>
            </div>
          </div>
          <div class="table-container">
            <table class="styled-table">
              <thead>
                <tr>
                  <th v-for="(value, key) in records[0]" :key="key">
                    {{ key }}
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="record in records"
                  :key="record.id"
                  @click="selectRecord(record)"
                  :class="{ selected: record === selectedRecord }"
                >
                  <td v-for="(value, key) in record" :key="key">{{ value }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div v-else-if="selectedTable && records.length === 0">
          <p class="empty-message">No records found for the selected table.</p>
        </div>

        <div v-else>
          <p class="welcome-message">Select a table to view its records.</p>
        </div>
      </section>

      <!-- Popup Modal -->
      <div v-if="showModal" class="modal-overlay">
        <div class="modal">
          <h2>{{ modalType === "add" ? "Add New Record" : "Edit Record" }}</h2>
          <form @submit.prevent="handleSubmit">
            <div
              v-for="(value, key) in modalRecord"
              :key="key"
              class="form-group"
            >
              <label :for="key">{{ key }}</label>
              <input
                type="text"
                :id="key"
                v-model="modalRecord[key]"
                :disabled="key === 'id' && modalType === 'edit'"
              />
            </div>
            <div class="modal-actions">
              <button type="submit" class="btn btn-save">💾 Save</button>
              <button type="button" class="btn btn-cancel" @click="closeModal">
                ✖️ Cancel
              </button>
            </div>
          </form>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      tables: [], // List of tables
      records: [], // Records in the selected table
      selectedTable: null, // Selected table name
      loading: false, // Loading state
      selectedRecord: null, // Selected record for updates/deletion
      showModal: false, // Controls modal visibility
      modalType: "", // Modal type: 'add' or 'edit'
      modalRecord: {}, // Holds the record being added or edited
    };
  },
  methods: {
    async fetchTables() {
      this.loading = true;
      try {
        const response = await axios.get("/admin/tables"); // Backend endpoint
        this.tables = response.data.tables; // Assume response contains { tables: [...] }
      } catch (error) {
        console.error("Error fetching tables:", error);
      } finally {
        this.loading = false;
      }
    },
    // Fetch records for the selected table
    async fetchTableRecords(table) {
      this.selectedTable = table;
      this.loading = true;
      try {
        const response = await axios.get(`/admin/tables/${table}/records`); // Backend endpoint
        this.records = response.data.records; // Assume response contains { records: [...] }
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
      this.modalRecord =
        type === "edit"
          ? { ...this.selectedRecord }
          : this.initializeEmptyRecord();
    },
    initializeEmptyRecord() {
      // Create an empty record structure based on the keys of the first record
      const emptyRecord = {};
      if (this.records.length > 0) {
        Object.keys(this.records[0]).forEach((key) => {
          emptyRecord[key] = "";
        });
      }
      return emptyRecord;
    },
    closeModal() {
      this.showModal = false;
    },
    async handleSubmit() {
      try {
        if (this.modalType === "add") {
          const response = await axios.post(
            `/api/admin/tables/${this.selectedTable}/records`,
            this.modalRecord
          );
          this.records.push(response.data);
          alert("Record added successfully!");
        } else if (this.modalType === "edit") {
          const response = await axios.put(
            `/api/admin/tables/${this.selectedTable}/records/${this.modalRecord.id}`,
            this.modalRecord
          );
          this.records = this.records.map((record) =>
            record.id === response.data.id ? response.data : record
          );
          alert("Record updated successfully!");
        }
      } catch (error) {
        console.error("Error saving record:", error);
      } finally {
        this.closeModal();
      }
    },
    async deleteRecord() {
      if (!this.selectedRecord) {
        alert("Please select a record to delete.");
        return;
      }
      const confirmDelete = confirm(
        `Are you sure you want to delete the record (id=${this.selectedRecord.id}) from ${this.selectedTable}?`
      );
      if (confirmDelete) {
        try {
          await axios.delete(
            `/api/admin/tables/${this.selectedTable}/records/${this.selectedRecord.id}`
          );
          this.records = this.records.filter(
            (record) => record.id !== this.selectedRecord.id
          );
          this.selectedRecord = null;
          alert("Record deleted successfully!");
        } catch (error) {
          console.error("Error deleting record:", error);
        }
      }
    },
  },
  mounted() {
    this.fetchTables();
  },
};
</script>

<style scoped>
/* Add same styles from previous version */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

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
</style>
