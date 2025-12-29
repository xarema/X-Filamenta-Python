/*
 * Purpose: Tabulator.js Configuration
 * Description: Configuration and utilities for Tabulator data grid library
 *
 * File: frontend/static/js/plugins/tabulator.js | Repository: X-Filamenta-Python
 * Created: 2025-12-27T00:00:00+00:00
 * Last modified (Git): TBD | Commit: TBD
 *
 * Distributed by: XAREMA | Coder: AleGabMar
 * App version: 0.0.1-Alpha | File version: 0.0.1-Alpha
 *
 * License: AGPL-3.0-or-later
 * SPDX-License-Identifier: AGPL-3.0-or-later
 *
 * Copyright (c) 2025 XAREMA. All rights reserved.
 *
 * Metadata:
 * - Status: Draft
 * - Classification: Public
 *
 * Notes:
 * - ES6+ JavaScript
 * - Tabulator 5.x compatible
 * - Global configuration and helper functions
 * - HTMX integration for dynamic updates
 */

/**
 * Tabulator.js Configuration
 * Configuration et utilitaires pour Tabulator
 */

// Configuration Tabulator par défaut
window.tabulatorDefaults = {
  layout: 'fitColumns',
  responsiveLayout: 'hide',
  pagination: 'local',
  paginationSize: 10,
  paginationSizeSelector: [10, 25, 50, 100],
  movableColumns: true,
  resizableRows: true,
  headerFilterPlaceholder: 'Filtrer...',
  locale: 'fr',
  langs: {
    'fr': {
      'pagination': {
        'first': 'Premier',
        'first_title': 'Première page',
        'last': 'Dernier',
        'last_title': 'Dernière page',
        'prev': 'Précédent',
        'prev_title': 'Page précédente',
        'next': 'Suivant',
        'next_title': 'Page suivante',
        'page_size': 'Taille de page'
      }
    }
  }
};

// Helper pour initialiser un tableau
function initTabulator(selector, columns, data = []) {
  if (typeof Tabulator === 'undefined') {
    console.warn('Tabulator not loaded');
    return null;
  }

  return new Tabulator(selector, {
    ...window.tabulatorDefaults,
    columns: columns,
    data: data
  });
}

// Export
window.tabulatorUtils = {
  init: initTabulator,
  defaults: window.tabulatorDefaults
};

console.log('Tabulator utilities loaded');

