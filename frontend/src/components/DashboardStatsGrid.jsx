import React, { useEffect, useState } from 'react'
import { IoBagHandle, IoPieChart, IoPeople, IoCart, IoClose } from 'react-icons/io5'
import api from '../api'

export default function DashboardStatsGrid() {
	const [isModalVisible, setIsModalVisible] = useState(false)
	const [newVersion, setNewVersion] = useState("")
	const [currentVersion, setCurrentVersion] = useState("")

	useEffect(() => {
		checkForUpdates()
	}, [])

	const checkForUpdates = async () => {
		console.log("checking for updates!")
		try {
			const res = await api.get("api/system/updates/")
			setNewVersion(res.data.new_version)
			setCurrentVersion(res.data.current_version)
			setIsModalVisible(true)
		} catch (error) {
			console.log(error)
		}
	}
	const handleUpdate = async () => {
		try {
			const data = {
				update: true,
				new_version: newVersion
			}
			await api.post("api/system/update/", data)
			setIsModalVisible(false)
		} catch (error) {
			console.log(error)
		}
	}
	return (
		<div>
			{isModalVisible && (
				<UpdateModal 
					currentVersion={currentVersion}
					newVersion={newVersion}
					onClose={() => setIsModalVisible(false)} 
					onUpdate={handleUpdate} 
				/>
			)}
		<div className="flex gap-4">
			<BoxWrapper>
				<div className="rounded-full h-12 w-12 flex items-center justify-center bg-sky-500">
					<IoBagHandle className="text-2xl text-white" />
				</div>
				<div className="pl-4">
					<span className="text-sm text-gray-500 font-light">Total Sales</span>
					<div className="flex items-center">
						<strong className="text-xl text-gray-700 font-semibold">$54232</strong>
						<span className="text-sm text-green-500 pl-2">+343</span>
					</div>
				</div>
			</BoxWrapper>
			<BoxWrapper>
				<div className="rounded-full h-12 w-12 flex items-center justify-center bg-orange-600">
					<IoPieChart className="text-2xl text-white" />
				</div>
				<div className="pl-4">
					<span className="text-sm text-gray-500 font-light">Total Expenses</span>
					<div className="flex items-center">
						<strong className="text-xl text-gray-700 font-semibold">$3423</strong>
						<span className="text-sm text-green-500 pl-2">-343</span>
					</div>
				</div>
			</BoxWrapper>
			<BoxWrapper>
				<div className="rounded-full h-12 w-12 flex items-center justify-center bg-yellow-400">
					<IoPeople className="text-2xl text-white" />
				</div>
				<div className="pl-4">
					<span className="text-sm text-gray-500 font-light">Total Customers</span>
					<div className="flex items-center">
						<strong className="text-xl text-gray-700 font-semibold">12313</strong>
						<span className="text-sm text-red-500 pl-2">-30</span>
					</div>
				</div>
			</BoxWrapper>
			<BoxWrapper>
				<div className="rounded-full h-12 w-12 flex items-center justify-center bg-green-600">
					<IoCart className="text-2xl text-white" />
				</div>
				<div className="pl-4">
					<span className="text-sm text-gray-500 font-light">Total Orders</span>
					<div className="flex items-center">
						<strong className="text-xl text-gray-700 font-semibold">16432</strong>
						<span className="text-sm text-red-500 pl-2">-43</span>
					</div>
				</div>
			</BoxWrapper>
		</div>
		</div>
	)
}

function BoxWrapper({ children }) {
	return <div className="bg-white rounded-sm p-4 flex-1 border border-gray-200 flex items-center">{children}</div>
}

function UpdateModal({ currentVersion, newVersion, onClose, onUpdate }) {
	return (
		<div className="fixed inset-0 flex items-start justify-center bg-black bg-opacity-50 z-50">
			<div className="bg-white rounded-lg p-6 w-full max-w-md mt-7 shadow-lg transform transition-all duration-300 ease-in-out relative">
				<button 
					className="absolute top-2 right-2 text-gray-400 hover:text-gray-600 transition-colors duration-150"
					onClick={onClose}
				>
					<IoClose size={20} />
				</button>
				<h2 className="text-xl font-semibold text-gray-800 mb-2">Update Available</h2>
				<p className="text-sm text-gray-600 mb-4">
					You are using version <strong>v.{currentVersion}</strong>. A new update version <strong>v.{newVersion}</strong> is available.
				</p>
				<button 
					className="w-full py-2 bg-blue-500 text-white font-medium rounded-md hover:bg-blue-600 transition-colors duration-200"
					onClick={onUpdate}
				>
					Click here to update
				</button>
			</div>
		</div>
	)
}