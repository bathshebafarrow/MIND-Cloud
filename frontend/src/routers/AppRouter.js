/**
 * Created on: 07/19/2025
 */
import React from 'react';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import NavBar from '../components/layout/NavBar/NavBar';
import CreateJobPage from '../views/CreateJob/CreateJobPage/CreateJobPage'
import HomePage from '../views/Home/HomePage/HomePage'
import NoPage from '../views/NoPage/NoPage'
import ViewJobsPage from '../views/ViewJobs/ViewJobsPage/ViewJobsPage'

const AppRouter = () => {
  return (
    <BrowserRouter>
        <NavBar />
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route index element={<HomePage />} />
          <Route path="create-job" element={<CreateJobPage />} />
          <Route path="view-jobs" element={<ViewJobsPage />} />
          <Route path="*" element={<NoPage />} />
        </Routes>
    </BrowserRouter>
  );
};

export default AppRouter;