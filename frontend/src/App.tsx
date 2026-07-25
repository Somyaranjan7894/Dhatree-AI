import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { AuthProvider, ProtectedRoute } from "@/modules/auth";
import { Layout } from "@/components/layout";
import { Suspense, lazy } from "react";

// Lazy load pages for code splitting
const Dashboard = lazy(() => import("@/pages").then(m => ({ default: m.Dashboard })));
const Recommendations = lazy(() => import("@/pages").then(m => ({ default: m.Recommendations })));
const DiseaseDetection = lazy(() => import("@/pages").then(m => ({ default: m.DiseaseDetection })));
const NotFound = lazy(() => import("@/pages").then(m => ({ default: m.NotFound })));
const Login = lazy(() => import("@/pages").then(m => ({ default: m.Login })));
const Register = lazy(() => import("@/pages").then(m => ({ default: m.Register })));
const Farms = lazy(() => import("@/pages").then(m => ({ default: m.Farms })));
const FarmDetails = lazy(() => import("@/pages").then(m => ({ default: m.FarmDetails })));
const SoilRecords = lazy(() => import("@/pages").then(m => ({ default: m.SoilRecords })));
const Weather = lazy(() => import("@/pages").then(m => ({ default: m.Weather })));
const AIAssistant = lazy(() => import("@/pages").then(m => ({ default: m.AIAssistant })));
const Reports = lazy(() => import("@/pages").then(m => ({ default: m.Reports })));
const Notifications = lazy(() => import("@/pages").then(m => ({ default: m.Notifications })));
const UserDirectory = lazy(() => import("@/pages").then(m => ({ default: m.UserDirectory })));
const Profile = lazy(() => import("@/pages").then(m => ({ default: m.Profile })));

// Configure TanStack Query client with production defaults
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
      staleTime: 5 * 60 * 1000, // 5 minutes
    },
  },
});

export const App: React.FC = () => {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <BrowserRouter>
          <Suspense fallback={<div className="flex h-screen items-center justify-center"><div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-green-600"></div></div>}>
            <Routes>
              {/* Public Authentication Routes */}
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />

              {/* Application Main Layout & Routes */}
              <Route path="/" element={<Layout />}>
                <Route index element={<Dashboard />} />
                <Route path="dashboard" element={<Dashboard />} />
                <Route path="ai-assistant" element={<AIAssistant />} />
                <Route path="reports" element={<Reports />} />
                <Route path="notifications" element={<Notifications />} />
                <Route path="recommendations" element={<Recommendations />} />
                <Route path="disease-detection" element={<DiseaseDetection />} />
                <Route path="weather" element={<Weather />} />

                {/* Protected Routes Requiring Authentication/Roles */}
                <Route element={<ProtectedRoute />}>
                  <Route path="profile" element={<Profile />} />
                </Route>

                <Route element={<ProtectedRoute allowedRoles={["farmer", "agronomist", "admin"]} />}>
                  <Route path="farms" element={<Farms />} />
                  <Route path="farms/:id" element={<FarmDetails />} />
                  <Route path="farms/:id/soil-records" element={<SoilRecords />} />
                  <Route path="farms/:id/weather" element={<Weather />} />
                </Route>

                <Route element={<ProtectedRoute allowedRoles={["admin"]} />}>
                  <Route path="admin/users" element={<UserDirectory />} />
                </Route>

                <Route path="*" element={<NotFound />} />
              </Route>
            </Routes>
          </Suspense>
        </BrowserRouter>
      </AuthProvider>
    </QueryClientProvider>
  );
};

export default App;
