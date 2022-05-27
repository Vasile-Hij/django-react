import { Route, Redirect } from 'react-router-dom'

const PrivateRoute = ({children, ...rest}) => {
    const authenticated = false
    return(
        <Route {...rest}>{!authenticated ? <Redirect to="/login"/> : children} </Route>
    )
}

export default PrivateRoute;
