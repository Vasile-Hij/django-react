import React from 'react'

const LoginPage = () => {
  return (
    <div>
        <form>
            <input type="text" name='username' pacleholder="Enter username"></input>
            <input type="text" name='password' pacleholder="Enter password"></input>
            <input type="submit"></input>
        </form>
    </div>
  )
}

export default LoginPage