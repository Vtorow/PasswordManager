<script setup lang="ts">
import HeaderComponent from '@/components/header.vue'
import FooterComponent from '@/components/footer.vue'

const formData = ref({
  login: "",
  password: "",
})

const repeat_password = ref("")
let error = ref("")

const register = async () => {
  error.value = ""

  if (formData.value.login.trim() == "") {
    error.value = "Введите корректное имя пользователя"
    return
  }
  if (formData.value.password.trim() == "") {
    error.value = "Введите корректный пароль"
    return
  }
  if (repeat_password.value.trim() == "") {
    error.value = "Введите корректный повторный пароль"
    return
  }
  if (repeat_password.value != formData.value.password) {
    error.value = "Пароли не совпадают"
    return
  }

  await $fetch(`/user/`, {
    method: 'POST',
    baseURL: useRuntimeConfig().public.apiURL,
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(formData.value),
    onResponse({ request, response, options }) {
      if (!response.ok) return;
      localStorage.setItem('access_token', response._data.access_token);
      window.location.reload();
    },
    onResponseError({ request, response, options }) {
      if (response._data?.detail) {
        error.value = response._data.detail;
        return;
      }
      error.value = "Непредвиденная ошибка.";
    }
  });
}

</script>

<template>
  <HeaderComponent/>
  <section class="flex flex-col pb-16 bg-white">

    <section class="flex flex-col justify-center self-stretch pt-16 text-sm font-medium leading-5 text-black">
      <div
          class="flex justify-center items-center self-center px-16 w-full max-w-[1100px] max-md:px-5 max-md:max-w-full">
        <div class="flex flex-col max-w-full w-[600px]">
          <h1 class="self-center text-4xl font-bold leading-10 text-center max-md:max-w-full mb-10">Регистрация</h1>
          <div v-if="error" class="p-4 mb-4 mt-2 text-center text-sm text-red-800 rounded-lg bg-red-50" role="alert">
          <span class="font-medium">Ошибка!</span> {{ error }}
        </div>
          <form action="/register" method="post">
            <div class="mb-3">
              <label for="username" class="block mb-2 text-sm font-medium text-gray-900">Имя пользователя</label>
              <input v-model="formData.login" type="text" id="username" name="username"
                     class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
                     placeholder="Введите имя пользователя" required/>
            </div>
            <div class="mb-3">
              <label for="password1" class="block mb-2 text-sm font-medium text-gray-900">Пароль</label>
              <input v-model="formData.password" type="password" id="password1" name="password1"
                     class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
                     placeholder="Введите пароль" required/>
            </div>
            <div class="mb-3">
              <label for="password2" class="block mb-2 text-sm font-medium text-gray-900">Повторите пароль</label>
              <input v-model="repeat_password" type="password" id="password2" name="password2"
                     class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
                     placeholder="Введите пароль ещё раз" required/>
            </div>
            <button type="button" @click="register"
                    class="justify-center self-center p-3 mt-6 text-base leading-6 text-white whitespace-nowrap bg-black rounded-lg max-md:px-5">
              Зарегистрироваться
            </button>
          </form>
        </div>
      </div>
    </section>

    <FooterComponent/>
  </section>
</template>