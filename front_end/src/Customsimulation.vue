<template>
  <div class="container">

    <button class="go-back" @click="$router.push('/')">← Go Back</button>
    <!-- ...rest of your simulation project page... -->


    <!-- Project Context -->
    <section>
        <h1>Create Custom Simulation Project</h1>
      <h2>Project Context</h2>
      <div class="row">
        <div class="input-group">
          <label>Project Name</label>
          <input type="text" v-model="projectName" />
        </div>
        <div class="input-group">
          <label>Project Description</label>
          <input type="text" v-model="projectDesc" />
        </div>
      </div>
      <div id="locations-section">
        <label>Locations (Cities or Outlets)</label>
        <div class="dynamic-list">
          <div v-for="(location, idx) in locations" :key="idx" class="item-wrapper">
            <input type="text" v-model="location.name" placeholder="Enter location..." />
            <button class="delete-btn" @click="removeLocation(idx)">×</button>
          </div>
        </div>
        <button @click="addLocation" class="add-btn">+ Add Location</button>
      </div>
      <div id="warehouses-section">
        <label>Central Warehouse Locations</label>
        <div class="dynamic-list">
          <div v-for="(warehouse, idx) in warehouses" :key="idx" class="item-wrapper">
            <input type="text" v-model="warehouse.name" placeholder="Enter warehouse location..." />
            <button class="delete-btn" @click="removeWarehouse(idx)">×</button>
          </div>
        </div>
        <button @click="addWarehouse" class="add-btn">+ Add Warehouse</button>
      </div>
    </section>

    <!-- Products -->
    <section>
      <h2>Products</h2>
      <div class="dynamic-list">
        <div v-for="(product, idx) in products" :key="idx" class="item-wrapper">
          <div class="input-group" style="margin-bottom:0;">
            <label>Product Name</label>
            <input type="text" v-model="product.name" />
          </div>
          <div class="input-group" style="margin-bottom:0;">
            <label>Units/Measure</label>
            <input type="text" v-model="product.unit" />
          </div>
          <button class="delete-btn" @click="removeProduct(idx)">×</button>
        </div>
      </div>
      <button @click="addProduct" class="add-btn">+ Add Product</button>
    </section>

    <!-- Outlet Inventory -->
    <section>
      <h2>Outlet Inventory</h2>
      <div class="input-group">
        <label>Current Storage Amount</label>
        <input type="text" v-model="outletInventory.current" />
        <label>Daily Replenishment (Base)</label>
        <input type="text" v-model="outletInventory.replenishment" />
        <label>Max Warehouse Capacity</label>
        <input type="text" v-model="outletInventory.maxCapacity" />
      </div>
    </section>

    <!-- Central Hub Inventory -->
    <section>
      <h2>Central Hub Inventory</h2>
      <div class="input-group">
        <label>Current Storage Amount</label>
        <input type="text" v-model="centralHubInventory.current" />
      </div>
    </section>

    <!-- Event Schedule -->
    <section>
      <h2>Event Schedule</h2>
      <div class="dynamic-list">
        <div v-for="(event, idx) in events" :key="idx" class="item-wrapper">
          <div class="input-group" style="margin-bottom:0;">
            <label>Event Date</label>
            <input type="date" v-model="event.date" />
          </div>
          <div class="input-group" style="margin-bottom:0;">
            <label>Event Description</label>
            <input type="text" v-model="event.desc" />
          </div>
          <button class="delete-btn" @click="removeEvent(idx)">×</button>
        </div>
      </div>
      <button @click="addEvent" class="add-btn">+ Add Event</button>
    </section>

    <!-- Transport & Logistics -->
    <section>
      <h2>Transport & Logistics</h2>
      <div class="input-group">
        <label>Estimated Transport Time</label>
        <input type="text" v-model="transport.time" />
        <label>Transport Costs</label>
        <input type="text" v-model="transport.cost" />
      </div>
    </section>

    <!-- Customer Preferences -->
    <section>
      <h2>Customer Preferences</h2>
      <div class="input-group">
        <label>Preference Profiles</label>
        <input type="text" v-model="customerPreferences" />
      </div>
    </section>

    <!-- Simulation Parameters -->
    <section>
      <h2>Simulation Parameters</h2>
      <div class="row">
        <div class="input-group">
          <label>Simulation Start Date</label>
          <input type="date" v-model="simulationParams.startDate" />
        </div>
        <div class="input-group">
          <label>Simulation End Date</label>
          <input type="date" v-model="simulationParams.endDate" />
        </div>
        <div class="input-group">
          <label>Daily Step Size</label>
          <select v-model="simulationParams.stepSize">
            <option value="hourly">Hourly</option>
            <option value="daily">Daily</option>
          </select>
        </div>
      </div>
    </section>

    <!-- Controls -->
    <div class="action-buttons">
      <button class="save" @click="saveConfig">Save Configuration</button>
      <button class="run" @click="runSimulation">Run Simulation</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CustomSimulationProject',
  emits: ['go-back'],
  data() {
    return {
      projectName: '',
      projectDesc: '',
      locations: [],
      warehouses: [],
      products: [],
      events: [],
      outletInventory: {
        current: '',
        replenishment: '',
        maxCapacity: ''
      },
      centralHubInventory: {
        current: ''
      },
      transport: {
        time: '',
        cost: ''
      },
      customerPreferences: '',
      simulationParams: {
        startDate: '',
        endDate: '',
        stepSize: 'daily'
      }
    }
  },
  methods: {
    // Locations
    addLocation() {
      this.locations.push({ name: '' });
    },
    removeLocation(idx) {
      this.locations.splice(idx, 1);
    },

    // Warehouses
    addWarehouse() {
      this.warehouses.push({ name: '' });
    },
    removeWarehouse(idx) {
      this.warehouses.splice(idx, 1);
    },

    // Products
    addProduct() {
      this.products.push({ name: '', unit: '' });
    },
    removeProduct(idx) {
      this.products.splice(idx, 1);
    },

    // Events
    addEvent() {
      this.events.push({ date: '', desc: '' });
    },
    removeEvent(idx) {
      this.events.splice(idx, 1);
    },

    // Save/Run (stub for now)
    saveConfig() {
      alert('Configuration saved! (stub)');
    },
    runSimulation() {
      alert('Simulation started! (stub)');
    }
  }
}
</script>

<style scoped>
body {
  font-family: 'Segoe UI', sans-serif;
  background-color: #eaf6ff;
  margin: 0;
  padding: 20px;
}

.container {
  max-width: 1100px;
  margin: auto;
  background: white;
  padding: 30px 40px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

h1 {
  text-align: center;
  margin-bottom: 30px;
  color: #1A73E8;
}

h2 {
  color: #34495e;
  margin-top: 40px;
  margin-bottom: 20px;
  font-weight: 700;
}

/* General row layout for input groups */
.row {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

/* Input group styling */
.input-group {
  flex: 1 1 280px;
  display: flex;
  flex-direction: column;
  margin-bottom: 20px;
}

.input-group label {
  margin-bottom: 8px;
  font-weight: 600;
  color: #34495e;
}

.input-group input,
.input-group select {
  padding: 12px 14px;
  border-radius: 6px;
  border: 1px solid #ccc;
  font-size: 1rem;
  transition: border-color 0.3s ease;
}

.input-group input:focus,
.input-group select:focus {
  border-color: #1A73E8;
  outline: none;
}

/* Dynamic lists container (locations, warehouses, products, events) */
.dynamic-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 25px;
}

/* Each dynamic list item wrapper for positioning delete button */
.item-wrapper {
  display: flex;
  align-items: center;
  gap: 15px;
  width: 100%;
  padding: 8px 0;
  background-color: #f8f9fa;
  border-radius: 8px;
  margin-bottom: 2px;
}

/* Inputs inside dynamic list items fill width */
.item-wrapper input,
.item-wrapper select {
  flex: 1;
  min-width: 0;
  padding: 10px 14px;
  font-size: 1rem;
  border-radius: 6px;
  border: 1px solid #bbb;
}

/* Delete button styling */
.delete-btn {
  flex-shrink: 0;
  background: #e74c3c;
  color: white;
  border: none;
  border-radius: 50%;
  width: 28px;
  height: 28px;
  cursor: pointer;
  transition: background-color 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  line-height: 1;
  margin-left: 10px;
  user-select: none;
}

.delete-btn:hover {
  background: #c0392b;
}

/* Add button styling */
button.add-btn {
  background-color: #1A73E8;
  color: white;
  padding: 12px 22px;
  border-radius: 8px;
  border: none;
  font-weight: 700;
  font-size: 1rem;
  margin-top: 10px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  user-select: none;
}

button.add-btn:hover {
  background-color: #155abd;
}

/* General button styling */
button {
  cursor: pointer;
  border-radius: 8px;
  border: none;
  padding: 8px 14px;
  margin-top: 8px;
  font-weight: 600;
  transition: opacity 0.2s ease;
}

button:hover {
  opacity: 0.9;
}

button:active {
  transform: scale(0.98);
}

/* Action buttons (Save, Run etc) */
.action-buttons {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 40px;
}

.save {
  background-color: #3498db;
  color: white;
  padding: 14px 30px;
  font-size: 1.1rem;
}

.run {
  background-color: #27ae60;
  color: white;
  padding: 14px 30px;
  font-size: 1.1rem;
}
</style>
