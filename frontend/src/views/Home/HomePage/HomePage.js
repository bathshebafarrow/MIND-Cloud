/**
 * Created on: 07/19/2025
 */
import React from "react";

const HomePage = () => {
    return (
        <div class="container">
            <p>Welcome to the site for electroencephalogram (EEG) signal data preprocessing and analysis.</p>
            <p>Raw EEG data files from one of the selectable online repositories can be preprocessed on demand then downloaded for further analysis using the links above. Expansion of current capabilities as well as additional ones will be incorporated in the future.</p>
            <p>For more information about the OpenNeuro datasets, visit the <a href='https://openneuro.org/dashboard/datasets'>OpenNeuro</a> site.</p>
            <p>To learn more about our group's work, visit the <a href='https://nirdslab.github.io/'>NIRDS Lab</a> research page.</p>
        </div>
    );
}

export default HomePage;