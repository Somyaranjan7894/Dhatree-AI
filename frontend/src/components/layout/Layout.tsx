/* eslint-disable react-refresh/only-export-components */
import React from "react";
import { AppLayout, AppLayoutProps } from "./AppLayout";
import { useAuth } from "@/modules/auth";

export const Layout: React.FC<AppLayoutProps> = (props) => {
  const auth = useAuth();

  return (
    <AppLayout
      user={props.user !== undefined ? props.user : auth.user}
      onLogout={props.onLogout || auth.logout}
      {...props}
    />
  );
};

export * from "./AppLayout";
