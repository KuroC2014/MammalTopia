import React, { Suspense, useEffect, useState } from "react";
import { Space, Spin, Table, Typography, message } from 'antd';
import { ComposableMap, Geographies, Geography } from "react-simple-maps";
import { extractKeys } from "../utils/CommonUtils";
import { postSearch } from "../requests/api";
const { Title } = Typography;

const mockData = [
    {
      key: '1',
      name: 'John Brown',
      age: 32,
      address: 'New York No. 1 Lake Park',
      tags: ['nice', 'developer'],
    },
    {
      key: '2',
      name: 'Jim Green',
      age: 42,
      address: 'London No. 1 Lake Park',
      tags: ['loser'],
    },
    {
      key: '3',
      name: 'Joe Black',
      age: 32,
      address: 'Sydney No. 1 Lake Park',
      tags: ['cool', 'teacher'],
    },
    {
        key: '1',
        name: 'John Brown',
        age: 32,
        address: 'New York No. 1 Lake Park',
        tags: ['nice', 'developer'],
      },
      {
        key: '2',
        name: 'Jim Green',
        age: 42,
        address: 'London No. 1 Lake Park',
        tags: ['loser'],
      },
      {
        key: '3',
        name: 'Joe Black',
        age: 32,
        address: 'Sydney No. 1 Lake Park',
        tags: ['cool', 'teacher'],
      },
      {
        key: '1',
        name: 'John Brown',
        age: 32,
        address: 'New York No. 1 Lake Park',
        tags: ['nice', 'developer'],
      },
      {
        key: '2',
        name: 'Jim Green',
        age: 42,
        address: 'London No. 1 Lake Park',
        tags: ['loser'],
      },
      {
        key: '3',
        name: 'Joe Black',
        age: 32,
        address: 'Sydney No. 1 Lake Park',
        tags: ['cool', 'teacher'],
      },
      {
        key: '1',
        name: 'John Brown',
        age: 32,
        address: 'New York No. 1 Lake Park',
        tags: ['nice', 'developer'],
      },
      {
        key: '2',
        name: 'Jim Green',
        age: 42,
        address: 'London No. 1 Lake Park',
        tags: ['loser'],
      },
      {
        key: '3',
        name: 'Joe Black',
        age: 32,
        address: 'Sydney No. 1 Lake Park',
        tags: ['cool', 'teacher'],
      },
];

const geoUrl = "https://cdn.jsdelivr.net/npm/world-atlas@2/countries-50m.json";

function WorldMap () {

    const [dataList, setDataList] = useState([]);
    const [columns, setColumns] = useState([]);
    const [currentPage, setCurrentPage] = useState(1);
    const [dataCount, setDataCount] = useState(0);
    const [countryName, setCountryName] = useState('');

    useEffect(() => {
        if (!countryName) {
            return;
        }
        postSearch({
            type: 'Country',
            query: countryName,
            page: currentPage
        }).then((data) => {
            let _dataList = data.dataList;
            setDataCount(data.count);
            if (_dataList.length > 0) {
                const _columns = extractKeys(_dataList[0]);
                // console.log("here: " + JSON.stringify(_columns));
                setColumns(_columns);
                setDataList(_dataList);
            }
        }).catch((err) => {
            // let _dataList = mockData;
            // setDataCount(50);
            // if (_dataList.length > 0) {
            //     const _columns = extractKeys(_dataList[0]);
            //     // console.log("here: " + JSON.stringify(_columns));
            //     setColumns(_columns);
            //     setDataList(_dataList);
            // }
            message.error("Failed to query list!")
        })
    }, [currentPage, countryName]);

    const handleCountryClick = (geo) => {
        setCountryName(geo.properties.name);
    };
    
    const handlePageChange = (page) => {
        setCurrentPage(page);
    };

    const handleSelectedTitle = (countryName) => {
        if (countryName && countryName !== '') {
            return (
                <Title style={{ fontSize: '16px'}}>Your selected <i>{countryName}</i></Title>
            );
        }
        return (<Title style={{ fontSize: '16px'}}>Please select a country</Title>);
    }

    return (
        <Space style={{ width: '80%', minWidth: '80%'}} direction='vertical'>
            <div style={{ width: '100%'}}>
                <Suspense fallback={<Spin/>}>
                    <ComposableMap projectionConfig={{
                        rotate: [-10, 0, 0],
                        scale: 120
                    }}>
                    <Geographies geography={geoUrl}>
                        {({ geographies }) =>
                        geographies.map((geo) => (
                            <Geography key={geo.rsmKey} geography={geo} 
                            style={{
                                default: {
                                    fill: "#85E0E0",
                                    outline: "none"
                                },
                                hover: {
                                    fill: "#E02619",
                                    outline: "none"
                                },
                                pressed: {
                                    fill: "#E02619",
                                    outline: "none"
                                }
                                }}
                                onClick={() => handleCountryClick(geo)}
                            />
                        ))
                        }
                    </Geographies>
                    </ComposableMap>
                </Suspense>

                <Space style={{ width: '100%', minWidth: '100%'}} direction='vertical' align='center' size='large'>
                    
                    {handleSelectedTitle(countryName)}
                    
                    <Table 
                        dataSource={dataList} 
                        columns={columns} 
                        pagination={{
                            position: ['bottomRight'],
                            showSizeChanger: false,
                            current: currentPage,
                            total: dataCount,
                            pageSize: 10,
                            onChange: handlePageChange,
                        }}
                    />
                </Space>
            </div>
        </Space>    
    );
}

export default WorldMap;