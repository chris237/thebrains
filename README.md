# School Management Module

This repository contains an Odoo module dedicated to managing an academic structure
with multiple campuses. The module provides models for campuses, faculties,
specialities, and additional academic entities required to manage schedules and
staff assignments.

## Key Features

- Maintain the list of campuses with geolocation and staff assignments.
- Create faculties that can now operate across multiple campuses through a
  dedicated multi-selection field.
- Manage specialities, cursus, levels, semesters, and courses linked to the
  appropriate faculty.
- Track faculty heads with automatic synchronization of contact details.
- Access all records through list, form, and kanban views for efficient daily
  operations.

## Multi-Campus Faculties

When creating or editing a faculty, select all the campuses where the faculty is
established. This information is automatically reflected on the related campus
records, ensuring consistency across the application.

## Installation

1. Install the module in your Odoo instance (supported with the `hr` and `mail`
   applications).
2. Update the apps list and search for **School**.
3. Install the module and start organizing your academic schedules.

## License

This module is distributed under the LGPL-3 license.
