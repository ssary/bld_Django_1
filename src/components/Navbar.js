import React from 'react';
import {
    Link
  } from "react-router-dom";
export default function Navbar(){
    return(
    <nav className="navbar">
        <div className="mobileNav">
        <Link to="/">
            <img src={require("../images/logo-udemy.svg")} alt="udemy" width="91" height="34"></img>
        </Link>

        </div>

        <button type="button">Categories</button>
        
        <form className="search_bar">
            <button type="submit" className="search_submit"><img src={require("../images/seach_icon.png")} alt="search" width="28" height="28" /></button>
            <input type="text" placeholder="Search for anything" name="search" className="icon"/>
        </form>
            
        <button>Udemy Business</button>
        <button>Teach on Udemy</button>
        <button>
            <img src={require("../images/shopping-cart.png")} alt="cart" width="28" height="28"/>
        </button>
        <button className="LL">Log in</button>
        <button id="SignUp">Sign up</button>
        <button className="LL">
            <img src={require("../images/globe.png")} alt="globe" width="28" height="28"/>
        </button>
        <button className="mobileNav"><img src={require("../images/menu.png")} alt="menu" width="28" height="28" /></button>
    </nav>
    )
}