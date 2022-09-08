import React from "react";

export default function Header(){
    const NewtoUdemyStyle = {
        fontSize:'20px',
        fontWeight: "normal"
      };
    return(
    <div id='header_container'>
        <header>
            <div><p>New to Udemy?Lucky you.</p>
                <p style={NewtoUdemyStyle}>Courses start at $169.99.get your new-student offer before it expires.</p>
            </div>
            <img src={require("../images/hourglass.png")} alt="hourglass" width="20%" height="auto" id = "hourglass"/>
        </header>
    </div>
    )
}