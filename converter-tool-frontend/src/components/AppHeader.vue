<template>
	<header class="bg-gray-800 text-white">
		<nav class="mx-auto max-w-7xl px-2 sm:px-6 lg:px-8">
			<div class="relative flex h-16 items-center justify-between">
				<div class="flex flex-1 items-center justify-center sm:items-stretch sm:justify-start">
					<div class="text-xl font-semibold">
						File Converter
					</div>
				</div>

				<div class="hidden sm:block">
					<div class="flex space-x-4">
						<router-link
							v-for="item in navigation" :key="item.name"
							:to="item.href"
							class="rounded-md px-3 py-2 text-sm font-medium"
							:class="item.current ? 'bg-gray-900 text-white' : 'text-gray-300 hover:bg-gray-700 hover:text-white'"
							:aria-current="item.current ? 'page' : undefined"
						>
							{{ item.name }}
						</router-link>
					</div>
				</div>
			</div>
		</nav>
	</header>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

const navigation = computed(() =>
	router.getRoutes()
		.filter(r => r.meta.visible)
		.map(r => ({
			name: String(r.name),
			href: r.path,
			current: r.path === route.path
		}))
)
</script>
