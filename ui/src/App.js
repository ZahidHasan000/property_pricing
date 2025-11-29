import './App.css';
// import CreateUserForm from "./component/price";
import CreateUserForm from "./component/predict";
import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";

function App() {
  // const user = useSelector((state) => state.user);
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<CreateUserForm />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
