class CreateLinks < ActiveRecord::Migration
  def change
    create_table :links do |t|
      t.string :url
      t.string :type
      t.integer :uses
      t.integer :trustlevel
      t.references :version, index: true

      t.timestamps null: false
    end
    add_foreign_key :links, :versions
  end
end
