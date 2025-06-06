<template>
  <div>
    <div class="top-bar">
      <router-link to="/create">
        <button class="create-btn">Create</button>
      </router-link>
    </div>
    <!-- ...other main content... -->
  </div>
</template>

<script>
export default {
  name: 'HomePage'
}
</script>

<style scoped>
.top-bar {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  padding: 20px 40px 0 0;
  background: transparent;
}
.create-btn {
  background-color: #1A73E8;
  color: white;
  padding: 10px 26px;
  border-radius: 8px;
  border: none;
  font-weight: 700;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.2s;
}
.create-btn:hover {
  background-color: #155abd;
}
</style>
