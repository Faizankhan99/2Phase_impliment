import React, { PropsWithChildren } from 'react';
import Menu from './Menu';
import Nav from './Nav';

const Wrapper = (props: PropsWithChildren<any>) => {
    return (
        <div>
            <Nav />
            <div className="container-fluid">
                <Menu />
                <main className="col-md-9 ms-sm-auto col-lg-10 px-md-4">
                    {props.children}
                </main>
            </div>
        </div>

    );
};

export default Wrapper;