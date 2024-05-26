import type {IPassword} from "~/interfaces/password.interface";

export interface IUser {
  id: number,
  login: string,
  passwords: IPassword[]
}

export interface IUserCreate {
  login: string,
  password: string
}