/**
 * Created on: 07/19/2025
 */
import React, { Component } from "react";
import { NavLink } from 'react-router-dom';
import './NavBar.css';

const NavBar = () => {
    return (
        <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
            &nbsp;
            <NavLink to="/" className="nav-link" end>Home</NavLink>
            <NavLink to="/create-job" className="nav-link">Submit Job</NavLink>
            <NavLink to="/view-jobs" className="nav-link">View Jobs</NavLink>
        </nav>
    );
};
    
export default NavBar;

