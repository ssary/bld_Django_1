import React from "react";
export default function MainCourses(props){
    console.log(props.data);
    return(
        <section>
        <div id="Courses_head">
            <h1 style={{fontSize:'xx-large'}}> A broad selection of courses </h1>
            <p style={{fontSize:'larger'}}> Choose from 185,000 online video courses with new additions published every month </p>
            <div>
                <button>Python</button>
            </div>
        </div>
        <div id="main_courses">
            <p style={{fontWeight:'bolder'}}>Expand your career opportunities with Python</p>
            <p id= "coursesP2">Take one of Udemy’s range of Python courses and learn how to code using this incredibly useful language. Its simple syntax and readability makes Python perfect for Flask, Django, data science, and machine learning. You’ll learn how to build everything from games to sites to apps. Choose from a range of courses that will appeal to...</p>
            <button id="explore_course">Explore Python</button>
            <br/>
            <div className = "course-container"style={{display:'flex'}}>
            </div>
        </div>

        </section>
    )
}