class CreateVersions < ActiveRecord::Migration
  def change
    create_table :versions do |t|
      t.datetime :lastaccess
      t.integer :edition
      t.integer :size
      t.references :book, index: true

      t.timestamps null: false
    end
    add_foreign_key :versions, :books
  end
end
