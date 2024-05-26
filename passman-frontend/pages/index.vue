<script setup lang="ts">
import HeaderComponent from '@/components/header.vue'
import FooterComponent from '@/components/footer.vue'
import type {IUser} from "~/interfaces/user.inteface";
import {initFlowbite} from "flowbite";
import type {IPassword, IPasswordCreate} from "~/interfaces/password.interface";
import useAuthedFetch from "~/extensions/useAuthedFetch";

const currentUser = useState<IUser | null>('currentUser');
const refreshUser = useState('refreshUser');
const success = ref<string>("");
const error = ref<string>("");
const passError = ref<string>("");

const newPassword = ref<IPasswordCreate>({
  login: "",
  password: "",
  description: ""
});

const editPassword = ref<IPassword>({
  id: 0,
  login: "",
  password: "",
  description: ""
});

const setEditPassword = (password_id: number) =>
    editPassword.value = currentUser.value?.passwords.find((p) => p.id === password_id);

const savePassword = async (password_id) => {
  passError.value = "";
  success.value = "";

  if (editPassword.value.login.trim() == "") {
    passError.value = "Введите корректный логин"
    return
  }
  if (editPassword.value.password.trim() == "") {
    passError.value = "Введите корректный пароль"
    return
  }

  await useAuthedFetch(`/password/${editPassword.value.id}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(editPassword.value),
    onResponse({ request, response, options }) {
      if (!response.ok) return;
      success.value = `Пароль для ${response._data.login} успешно сохранён!`;
      editPassword.value = {
        id: 0,
        login: "",
        password: "",
        description: ""
      };
      refreshUser.value();
    },
    onResponseError({ request, response, options }) {
      if (response._data?.detail) {
        error.value = response._data.detail;
        return;
      }
      error.value = "Непредвиденная ошибка.";
      editPassword.value = {
        id: 0,
        login: "",
        password: "",
        description: ""
      };
    }
  })
}

const deletePassword = async (password_id: number) => {
  success.value = "";

  await useAuthedFetch(`/password/${password_id}`, {
    method: 'DELETE',
    onResponse({ request, response, options }) {
      if (!response.ok) return;
      success.value = `Пароль для ${response._data.login} успешно удалён!`;
      refreshUser.value();
    },
    onResponseError({ request, response, options }) {
      if (response._data?.detail) {
        error.value = response._data.detail;
        return;
      }
      error.value = "Непредвиденная ошибка.";
    }
  })
}

const addPassword = async () => {
  passError.value = "";
  success.value = "";

  if (newPassword.value.login.trim() == "") {
    passError.value = "Введите корректный логин"
    return
  }
  if (newPassword.value.password.trim() == "") {
    passError.value = "Введите корректный пароль"
    return
  }

  await useAuthedFetch(`/password/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(newPassword.value),
    onResponse({ request, response, options }) {
      if (!response.ok) return;
      success.value = `Пароль для ${response._data.login} успешно создан!`;
      newPassword.value = {
        login: "",
        password: "",
        description: ""
      };
      refreshUser.value();
    },
    onResponseError({ request, response, options }) {
      if (response._data?.detail) {
        error.value = response._data.detail;
        return;
      }
      error.value = "Непредвиденная ошибка.";
      newPassword.value = {
        login: "",
        password: "",
        description: ""
      };
    }
  })
}

onMounted(() => {
  initFlowbite();
})
</script>

<template>
  <HeaderComponent/>

  <div class="w-full flex justify-center mt-20">
    <div class="container w-full">
      <div class="w-full flex justify-between items-center">
        <h1 class="text-2xl font-bold">Здравствуйте, {{ currentUser.login }}! Ваши пароли:</h1>
        <button type="button" data-modal-target="add-modal" data-modal-toggle="add-modal"
                class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 me-2 mb-2 dark:bg-blue-600 dark:hover:bg-blue-700 focus:outline-none dark:focus:ring-blue-800">
          Добавить пароль
        </button>
      </div>

      <div v-if="success" class="p-4 mb-4 text-sm text-green-800 rounded-lg bg-green-50 dark:bg-gray-800 dark:text-green-400" role="alert">
        <span class="font-medium">Успешно!</span> {{ success }}
      </div>
      <div v-if="error" class="p-4 mb-4 text-sm text-red-800 rounded-lg bg-red-50 dark:bg-gray-800 dark:text-red-400" role="alert">
        <span class="font-medium">Ошибка!</span> {{ error }}
      </div>

      <div class="relative overflow-x-auto shadow-md sm:rounded-lg mt-10">
        <table class="w-full text-sm text-left rtl:text-right text-gray-500 dark:text-gray-400">
          <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
          <tr>
            <th scope="col" class="px-6 py-3">
              ID
            </th>
            <th scope="col" class="px-6 py-3">
              Логин
            </th>
            <th scope="col" class="px-6 py-3">
              Пароль
            </th>
            <th scope="col" class="px-6 py-3">
              Описание
            </th>
            <th scope="col" class="px-6 py-3">
              Действия
            </th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="password in currentUser.passwords" :key="password.id"
              class="odd:bg-white odd:dark:bg-gray-900 even:bg-gray-50 even:dark:bg-gray-800 border-b dark:border-gray-700">
            <th scope="row" class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white">
              {{ password.id }}
            </th>
            <td class="px-6 py-4">
              {{ password.login }}
            </td>
            <td class="px-6 py-4">
              {{ password.password }}
            </td>
            <td class="px-6 py-4">
              {{ password.description }}
            </td>
            <td class="px-6 py-4 flex items-center gap-5">
              <a @click="setEditPassword(password.id)" data-modal-target="edit-modal" data-modal-toggle="edit-modal" class="cursor-pointer font-medium text-blue-600 dark:text-blue-500 hover:underline">Редактировать</a>
              <a @click="deletePassword(password.id)" class="cursor-pointer font-medium text-red-600 dark:text-red-500 hover:underline">Удалить</a>
            </td>
          </tr>
          </tbody>
        </table>
      </div>

    </div>
  </div>

  <div id="add-modal" tabindex="-1" aria-hidden="true"
       class="hidden overflow-y-auto overflow-x-hidden fixed top-0 right-0 left-0 z-50 justify-center items-center w-full md:inset-0 h-[calc(100%-1rem)] max-h-full">
    <div class="relative p-4 w-full max-w-2xl max-h-full">
      <div class="relative bg-white rounded-lg shadow dark:bg-gray-700">
        <div class="flex items-center justify-between p-4 md:p-5 border-b rounded-t dark:border-gray-600">
          <h3 class="text-xl font-semibold text-gray-900 dark:text-white">
            Добавить пароль
          </h3>
          <button type="button"
                  class="text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm w-8 h-8 ms-auto inline-flex justify-center items-center dark:hover:bg-gray-600 dark:hover:text-white"
                  data-modal-hide="add-modal">
            <svg class="w-3 h-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 14">
              <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6"/>
            </svg>
            <span class="sr-only">Закрыть</span>
          </button>
        </div>
        <form class="p-4 md:p-5">
            <div v-if="passError" class="p-4 mb-4 text-sm text-red-800 rounded-lg bg-red-50 dark:bg-gray-800 dark:text-red-400" role="alert">
              {{ passError }}
            </div>
            <div class="grid gap-4 mb-4 grid-cols-2">
              <div class="col-span-2">
                <label for="login" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Логин</label>
                <input v-model="newPassword.login" type="text" name="login" id="login" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500" placeholder="Логин" required="">
              </div>
              <div class="col-span-2">
                <label for="password" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Пароль</label>
                <input v-model="newPassword.password" type="password" name="password" id="password" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500" placeholder="Пароль" required="">
              </div>
              <div class="col-span-2">
                <label for="description" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Описание (необязательно)</label>
                <input v-model="newPassword.description" type="text" name="description" id="description" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500" placeholder="Описание" required="">
              </div>
            </div>
          </form>
        <div class="flex items-center p-4 md:p-5 border-t border-gray-200 rounded-b dark:border-gray-600">
          <button @click="addPassword" type="button"
                  class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">
            Создать
          </button>
          <button data-modal-hide="add-modal" type="button"
                  class="py-2.5 px-5 ms-3 text-sm font-medium text-gray-900 focus:outline-none bg-white rounded-lg border border-gray-200 hover:bg-gray-100 hover:text-blue-700 focus:z-10 focus:ring-4 focus:ring-gray-100 dark:focus:ring-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:border-gray-600 dark:hover:text-white dark:hover:bg-gray-700">
            Отменить
          </button>
        </div>
      </div>
    </div>
  </div>

  <div id="edit-modal" tabindex="-1" aria-hidden="true"
       class="hidden overflow-y-auto overflow-x-hidden fixed top-0 right-0 left-0 z-50 justify-center items-center w-full md:inset-0 h-[calc(100%-1rem)] max-h-full">
    <div class="relative p-4 w-full max-w-2xl max-h-full">
      <div class="relative bg-white rounded-lg shadow dark:bg-gray-700">
        <div class="flex items-center justify-between p-4 md:p-5 border-b rounded-t dark:border-gray-600">
          <h3 class="text-xl font-semibold text-gray-900 dark:text-white">
            Добавить пароль
          </h3>
          <button type="button"
                  class="text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm w-8 h-8 ms-auto inline-flex justify-center items-center dark:hover:bg-gray-600 dark:hover:text-white"
                  data-modal-hide="edit-modal">
            <svg class="w-3 h-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 14">
              <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6"/>
            </svg>
            <span class="sr-only">Закрыть</span>
          </button>
        </div>
        <form class="p-4 md:p-5">
            <div v-if="passError" class="p-4 mb-4 text-sm text-red-800 rounded-lg bg-red-50 dark:bg-gray-800 dark:text-red-400" role="alert">
              {{ passError }}
            </div>
            <div class="grid gap-4 mb-4 grid-cols-2">
              <div class="col-span-2">
                <label for="login" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Логин</label>
                <input v-model="editPassword.login" type="text" name="login" id="login" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500" placeholder="Логин" required="">
              </div>
              <div class="col-span-2">
                <label for="password" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Пароль</label>
                <input v-model="editPassword.password" type="password" name="password" id="password" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500" placeholder="Пароль" required="">
              </div>
              <div class="col-span-2">
                <label for="description" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Описание (необязательно)</label>
                <input v-model="editPassword.description" type="text" name="description" id="description" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500" placeholder="Описание" required="">
              </div>
            </div>
          </form>
        <div class="flex items-center p-4 md:p-5 border-t border-gray-200 rounded-b dark:border-gray-600">
          <button @click="savePassword" type="button"
                  class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">
            Сохранить
          </button>
          <button data-modal-hide="edit-modal" type="button"
                  class="py-2.5 px-5 ms-3 text-sm font-medium text-gray-900 focus:outline-none bg-white rounded-lg border border-gray-200 hover:bg-gray-100 hover:text-blue-700 focus:z-10 focus:ring-4 focus:ring-gray-100 dark:focus:ring-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:border-gray-600 dark:hover:text-white dark:hover:bg-gray-700">
            Отменить
          </button>
        </div>
      </div>
    </div>
  </div>

  <FooterComponent/>
</template>
