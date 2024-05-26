<script setup lang="ts">
import type {IUser} from "~/interfaces/user.inteface";

const currentUser = useState<IUser | null>('currentUser');

const logout = () => {
  localStorage.removeItem("access_token");
  window.location.reload();
}

</script>

<template>
  <header class="flex gap-5 justify-center items-center p-5 text-black bg-white shadow-sm max-md:flex-wrap">
    <div class="container flex gap-5 justify-center items-center text-black bg-white max-md:flex-wrap">
        <a href="/" class="flex-1 self-stretch my-auto text-2xl leading-9 max-md:max-w-full font-bold">PassMan</a>
        <div v-if="!currentUser" class="flex gap-2 mx-2 justify-center">
            <a href="/login" class="text-white bg-green-700 hover:bg-green-800 focus:outline-none focus:ring-4 focus:ring-green-300 font-medium rounded-full text-sm px-5 py-2.5 text-center me-2 mb-2 dark:bg-green-600 dark:hover:bg-green-700 dark:focus:ring-green-800">Вход</a>
            <a href="/register" class="text-white bg-blue-700 hover:bg-blue-800 focus:outline-none focus:ring-4 focus:ring-blue-300 font-medium rounded-full text-sm px-5 py-2.5 text-center me-2 mb-2 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">Регистрация</a>
        </div>
        <a v-else href="#" class="flex gap-2 mx-5 justify-center items-center hover:underline">
            <p>{{ currentUser.login }}</p>
            <button @click="logout" type="button" class="text-white bg-red-700 hover:bg-red-800 focus:outline-none focus:ring-4 focus:ring-red-300 font-medium rounded-full text-sm px-5 py-2.5 text-center me-2 mb-2">Выход</button>
        </a>
    </div>
</header>
</template>