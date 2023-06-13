<template>
  <div>
    <NavigationBar/>
    <br><br>
    <DropZone/>
  </div>
</template>

<script>
import NavigationBar from './components/NavigationBar.vue'
import DropZone from './components/DropZone.vue'


export default {
  name: 'App',
  components: {
    NavigationBar,
    DropZone,
  }
}

</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>
