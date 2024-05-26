
export interface IPasswordCreate {
  login: string,
  password: string,
  description: string
}

export interface IPassword extends IPasswordCreate{
  id: number
}