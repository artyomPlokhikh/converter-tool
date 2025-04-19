import { createRouter, createWebHistory } from 'vue-router'

const routes = [
	{ path: '/', redirect: '/image' },
	{
		path: '/image',
		name: 'image',
		meta: { visible: true },
		component: () => import('@/components/converters/ImageConverter.vue'),
	},
	{
		path: '/audio',
		name: 'audio',
		meta: { visible: true },
		component: () => import('@/components/converters/AudioConverter.vue'),
	},
	{ path: '/:pathMatch(.*)*', redirect: '/image' },
]

const router = createRouter({
	history: createWebHistory(import.meta.env.BASE_URL),
	routes,
})

export default router
