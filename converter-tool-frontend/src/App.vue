<template>
	<div class="min-h-screen flex flex-col">
		<app-header/>

		<main class="flex-1 container mx-auto p-4">
			<router-view/>
		</main>

		<app-footer/>
	</div>
</template>

<script setup>
import AppHeader from './components/AppHeader.vue'
import AppFooter from './components/AppFooter.vue'

</script>
