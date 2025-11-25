"use client";

import React, { useEffect, useState } from "react";
import axios from "axios";


// eslint-disable-next-line @typescript-eslint/no-explicit-any
type Item = Record<string, any>;

export default function PublicBusinessPageAi() {
  const [items, setItems] = useState<Item[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const controller = new AbortController();
    // eslint-disable-next-line react-hooks/set-state-in-effect
    setLoading(true);
    setError(null);

    // Replace '/api/items' with your real endpoint (or use process.env.NEXT_PUBLIC_API_URL)
    axios
      .get<Item[]>("https://localhost:5000/business/product", { signal: controller.signal })
      .then((res) => setItems(res.data ?? []))
      .catch((err) => {
        if (!axios.isCancel(err)) {
          setError(err?.message ?? "Failed to load items");
        }
      })
      .finally(() => setLoading(false));

    return () => controller.abort();
  }, []);

  // determine columns from first item (or all keys union)
  const columns = React.useMemo(() => {
    const keys = new Set<string>();
    items.forEach((it) => Object.keys(it ?? {}).forEach((k) => keys.add(k)));
    return Array.from(keys);
  }, [items]);

  return (
    <div className="flex min-h-screen items-center justify-center bg-zinc-50 font-sans dark:bg-black">
      <main className="flex min-h-screen w-full max-w-4xl flex-col items-center justify-start py-12 px-6 bg-white dark:bg-black sm:items-start">
        <h1 className="mb-6 text-2xl font-semibold text-black dark:text-zinc-50">
          Business Page
        </h1>

        {loading ? (
          <div className="text-sm text-zinc-500">Loading...</div>
        ) : error ? (
          <div className="text-sm text-red-500">Error: {error}</div>
        ) : items.length === 0 ? (
          <div className="text-sm text-zinc-500">No items found</div>
        ) : (
          <div className="w-full overflow-x-auto">
            <table className="min-w-full table-auto divide-y divide-zinc-200 dark:divide-zinc-700">
              <thead className="bg-zinc-100 dark:bg-zinc-900">
                <tr>
                  {columns.map((col) => (
                    <th
                      key={col}
                      className="px-4 py-2 text-left text-xs font-medium uppercase text-zinc-600 dark:text-zinc-300"
                    >
                      {col}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody className="divide-y divide-zinc-100 bg-white dark:bg-black">
                {items.map((item, idx) => (
                  <tr key={idx} className="hover:bg-zinc-50 dark:hover:bg-zinc-900">
                    {columns.map((col) => {
                      const value = item?.[col];
                      // Render primitive values directly, objects/arrays as JSON
                      const cell =
                        value === null || value === undefined
                          ? "-"
                          : typeof value === "string" || typeof value === "number" || typeof value === "boolean"
                          ? String(value)
                          : JSON.stringify(value);
                      return (
                        <td key={col} className="px-4 py-2 text-sm text-zinc-700 dark:text-zinc-200">
                          {cell}
                        </td>
                      );
                    })}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </main>
    </div>
  );
}
