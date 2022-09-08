import './App.css';
import Navbar from './components/Navbar';
import Header from './components/Header';
import MainCourses from './components/MainCourses';
import {useEffect, useState} from 'react'

function App() {
  const [courses,setCourses] = useState();
  
  useEffect(()=>{
    fetch('http://localhost:4000/data')
      .then((res)=>res.json())
      .then((data)=>{setCourses(data['python_res']);})
      
  },[])
  return (
    <>
    <Navbar/>
    <Header/>
    <MainCourses data={courses}/>
    </>
  );
}

export default App;
