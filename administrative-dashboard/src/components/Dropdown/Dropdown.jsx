import { useState } from "react"

function Dropdown({ label, options, onSelect }) {
    const [open, setOpen] = useState(false)
    const [selected, setSelected] = useState(label)

    function handleSelect(option) {
        setSelected(option.label)
        onSelect(option.value)
        setOpen(false)
    }

    return (
        <div className="relative inline-block">
            <button
                onClick={() => setOpen(!open)}
                className="flex items-center gap-2 px-4 py-2 bg-white border border-gray-200 rounded-lg text-sm font-medium hover:bg-gray-50"
            >
                {selected}
                <span className={`transition-transform ${open ? "rotate-180" : ""}`}>▾</span>
            </button>

            {open && (
                <ul className="absolute z-10 mt-1 w-48 bg-white border border-gray-200 rounded-lg shadow-lg">
                    {options.map(option => (
                        <li
                            key={option.value}
                            onClick={() => handleSelect(option)}
                            className="px-4 py-2 text-sm hover:bg-gray-50 cursor-pointer first:rounded-t-lg last:rounded-b-lg"
                        >
                            {option.label}
                        </li>
                    ))}
                </ul>
            )}
        </div>
    )
}

export default Dropdown