<template>
	<div class="max-w-md mx-auto">
		<h2 class="text-xl mb-4">Convert an Image</h2>
		<form @submit.prevent="onSubmit" class="space-y-4">
			<input
				type="file"
				accept="image/*"
				@change="onFileChange"
				class="block w-full"
			/>

			<select v-model="format" class="w-full border rounded p-2">
				<option
					v-for="opt in formats"
					:key="opt.value"
					:value="opt.value"
				>
					{{ opt.label }}
				</option>
			</select>

			<button
				type="submit"
				:disabled="!file"
				class="w-full bg-blue-600 text-white py-2 rounded disabled:opacity-50"
			>
				Convert
			</button>
		</form>
	</div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { convertImage } from '@/services/converterApi'

interface FormatOption {
	value: string
	label: string
}

const file = ref<File | null>(null)
const format = ref<string>('PNG')
const formats = <FormatOption[]>[
	{ value: 'JPEG', label: 'JPEG' },
	{ value: 'BMP', label: 'BMP' },
	{ value: 'GIF', label: 'GIF' },
	{ value: 'PNG', label: 'PNG' },
	{ value: 'ICO', label: 'ICO' },
]

function onFileChange(e: Event) {
	const input = e.target as HTMLInputElement
	if (input.files && input.files[0]) {
		file.value = input.files[0]
	}
}

async function onSubmit() {
	if (!file.value) return

	try {
		const blob = await convertImage(file.value, format.value)

		const url = URL.createObjectURL(blob)
		const a = document.createElement('a')
		a.href = url
		a.download = `converted.${format.value.toLowerCase()}`
		a.click()
		URL.revokeObjectURL(url)

	} catch (err) {
		console.error(err)
		alert('Failed to convert image.')
	}
}
</script>
