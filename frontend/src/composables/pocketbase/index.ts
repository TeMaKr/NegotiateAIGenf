import PocketBase from 'pocketbase'
import { ref } from 'vue'
import { Collections, type TypedPocketBase, type UsersResponse } from './types'

enum PocketCMBDQueryKeys {}

export const QueryEnumKeys = { ...PocketCMBDQueryKeys, ...Collections }

export const pb = new PocketBase(
  import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8090',
) as TypedPocketBase

pb.autoCancellation(false)

export const usePocketBase = async () => {
  const isAuthenticated = ref(pb.authStore.isValid)
  const user = ref<UsersResponse | null>(null)

  const refresh = async () => {
    if (pb.authStore.isValid && pb.authStore.record) {
      user.value = pb.authStore.record as UsersResponse
      return
    }
    user.value = null
  }

  await refresh()

  pb.authStore.onChange(async () => {
    isAuthenticated.value = pb.authStore.isValid
    await refresh()
  })

  return { isAuthenticated, user, refresh }
}

export { Collections }
