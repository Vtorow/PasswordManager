<template>
  <div>
    <NuxtPage />
  </div>
</template>

<script setup lang="ts">
import useAuthedFetch from "~/extensions/useAuthedFetch";
import type {IUser} from "~/interfaces/user.inteface";

const currentUser = useState<IUser | null>('currentUser');
const refreshUser = useState('refreshUser');
await callOnce(async () => {
  const { data, refresh } = await useAsyncData<IUser | null>(
    'currentUser',
    () => useAuthedFetch(`${useRuntimeConfig().public.apiURL}/user/me`)
  )
  refreshUser.value = refresh;
  currentUser.value = data;
  if (!data.value && localStorage.getItem("access_token")) {
    localStorage.removeItem("access_token");
    window.location.reload();
  }
})
</script>
