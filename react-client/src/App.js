import React from 'react';
import NavLinks from './NavLinks';

export default function App ({token}) { 
    console.log('access token:', token);
    
    return (
        <div>
            
            {/* Navbar */}
            <nav className="main-nav">
                <h1>Photo App</h1>
                <NavLinks token={token} />
            </nav>
           
           {/* Right Panel */}
            <aside>
                <header>
                    Profile Goes Here...
                </header>
                <div className="suggestions">
                    <div>
                        Suggestions go here...
                    </div>
                </div>
            </aside>

            <main>

                {/* Stories */}
                <header className="stories">
                    Stories go here...
                </header>

                {/* Posts */}
                <div id="posts">
                    Posts go here...
                </div>

            </main>

        </div>
    );
    
}