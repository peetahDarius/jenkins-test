import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import Layout from './components/shared/Layout'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import Products from './pages/Products'
import Login from './pages/Login'
import ProtectedRoute from './components/ProtectedRoutes'

function App() {
    return (
        <Router>
            <Routes>
            <Route path="/login" element={<Login />} />
                <Route path="/" element={<ProtectedRoute> <Layout /> </ProtectedRoute>}>
                    <Route index element={<ProtectedRoute> <Dashboard /> </ProtectedRoute>} />
                    <Route path="products" element={<ProtectedRoute> <Products /> </ProtectedRoute>} />
                    <Route path="logout" element={<ProtectedRoute> <Logout /> </ProtectedRoute>} />
                </Route>
                <Route path="/register" element={<RegisterAndLogout />} />
            </Routes>
        </Router>
    )
}
function Logout() {
    localStorage.clear();
    return <Navigate to="/login" />
}

function RegisterAndLogout() {
    localStorage.clear();
    return <Register />
}
export default App
